import json
import copy

from fastapi import APIRouter, Header, Depends, HTTPException

from sqlalchemy.orm import Session

from schema import AccountCreate, AccountRead, UsernameDto, PasswordDto, AttributeDto
from persistence.account import AccountService
from persistence.attribute import AttributeService
from persistence.session import SessionService
from api import API_PREFIX, get_db

router = APIRouter(
    prefix=f"{API_PREFIX}/account"
)

with open("config/config.json", "r") as fp:
    _config = json.load(fp)

_attributes = {}
_required_attributes: set[str] = set()
for attribute in _config['attributes']:
    _attributes[attribute['key']] = attribute
    if attribute['required']:
        _required_attributes.add(attribute['key'])

_super = _config.get('super', [])

def _validate_username(dto: UsernameDto, db: Session):
    user = AccountService.read_account_by_username(db=db, username=dto.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

def _validate_password(dto: PasswordDto, db: Session):
    if dto.password != dto.password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords must match")

def _validate_token(db: Session, token: str):
    if token is None or token == "":
        _invalid_token(db=db)
    valid = SessionService.is_token_valid(db=db, session_id=token)
    if valid == False:
        _invalid_token(db=db)
    SessionService.prune_sessions(db=db)

def _invalid_token(db: Session):
    SessionService.prune_sessions(db=db)
    raise HTTPException(status_code=401, detail="Invalid token")

def _no_such_attribute(attribute: str):
    raise HTTPException(status_code=404, detail=f"No such attribute '{attribute}'")

def _read_sensitive_attribute(attribute: str):
    raise HTTPException(status_code=401, detail=f"Cannot read sensitive attribute '{attribute}'")

def _sensitive(attribute: str) -> bool:
    try:
        return _attributes[attribute]['sensitive']
    except KeyError:
        _no_such_attribute(attribute)

def _unique(attribute: str) -> bool:
    try:
        return _attributes[attribute]['unique']
    except KeyError:
        _no_such_attribute(attribute)

def _required(attribute: str) -> bool:
    try:
        return _attributes[attribute]['required']
    except KeyError:
        _no_such_attribute(attribute)

@router.post("/")
def create_account(dto: AccountCreate, db: Session = Depends(get_db)):
    _validate_username(db=db, dto=dto)
    _validate_password(db=db, dto=dto)

    # Validate that all required attributes are hit
    processed: list[AttributeDto] = []
    visited: set[str] = set()
    attributes_needed: set[str] = copy.copy(_required_attributes)
    unique_attributes: list[AttributeDto] = []
    for attribute in dto.attributes:
        if attribute.key not in _attributes.keys() or attribute.key in visited:
            continue
        visited.add(attribute.key)
        if attribute.key in attributes_needed:
            attributes_needed.remove(attribute.key)
        if _unique(attribute.key):
            unique_attributes.append(attribute)
        processed.append(attribute)

    if len(attributes_needed) > 0:
        missing = ''
        for missing_attribute in attributes_needed:
            missing += f"{missing_attribute} "
        raise HTTPException(status_code=400, detail=f"Attributes {missing}are required")
    
    # Validate that all unique attributes are unique
    for attribute in unique_attributes:
        account = AccountService.read_account_by_unique_attribute(
            db=db, key=attribute.key, value=attribute.value)
        if account is not None:
            raise HTTPException(status_code=409, detail=f"{attribute.key.capitalize()} '{attribute.value}' already in use.")
    dto.attributes = processed

    AccountService.create_account(db=db, account=dto)

@router.get("/", response_model=AccountRead)
def read_account(db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    db_account = SessionService.read_session_bearer(db=db, session_id=token)
    SessionService.update_session(db=db, session_id=token)
    return db_account

@router.get("/account/{username}", response_model=AccountRead)
def read_account_by_username(username: str, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    return AccountService.read_account_by_username(db=db, username=username)

@router.get("/account/attribute/{key}/{value}", response_model=AccountRead)
def read_account_by_unique_attribute(key: str, value: str, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)

    # Check that attribute is not sensitive
    if _sensitive(key):
        _read_sensitive_attribute(key)

    # Check that attribute is unique
    if not _unique(key):
        raise HTTPException(status_code=400, detail=f"Cannot read account by non-unique attribute '{key}'")

    account = AccountService.read_account_by_unique_attribute(db=db, key=key, value=value)
    if account is None:
        raise HTTPException(status_code=404, detail="No such account")
    
    return account

@router.get("/account/{account_id}/{attribute}", response_model=AttributeDto)
def read_account_attribute(account_id: int, attribute: str, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)

    # Check that attribute is not sensitive
    if _sensitive(attribute):
        account = read_account(token=token, db=db)
        if account.id not in _super and account.id != account_id:
            _read_sensitive_attribute(attribute)

    db_attribute = AttributeService.read_account_attribute(db=db, account_id=account_id, key=attribute)
    if db_attribute is None:
        raise HTTPException(status_code=404, detail="No match found")
    
    return db_attribute

@router.put("/username")
def update_username(dto: UsernameDto, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    _validate_username(db=db, dto=dto)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.update_username(db=db, account_id=account.id, dto=dto)
    SessionService.update_session(db=db, session_id=token)

@router.put("/password")
def update_password(dto: PasswordDto, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    _validate_password(db=db, dto=dto)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.update_password(db=db, account_id=account.id, dto=dto)
    SessionService.update_session(db=db, session_id=token)

@router.put("/account/attribute")
def update_attribute(dto: AttributeDto, db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    account = SessionService.read_session_bearer(db=db, session_id=token)

    # Verify that required attribute is not being unset
    if dto.value is None and _required(dto.key):
        raise HTTPException(status_code=400, detail=f"Cannot unset required attribute {dto.key}")

    AttributeService.update_account_attribute(db=db, account_id=account.id, attribute=dto)

@router.delete("/")
def delete_account(db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    SessionService.delete_sessions_by_account(db=db, account_id=account.id)
    AccountService.delete_account(db=db, account_id=account.id)
