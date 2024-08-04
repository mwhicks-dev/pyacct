from uuid import UUID

from fastapi import APIRouter, Header, Depends, HTTPException

from sqlalchemy.orm import Session

from schema.account import AccountCreate, AccountRead, UsernameDto, PasswordDto
from persistence.account import AccountService
from persistence.session import SessionService
from api.api import API_PREFIX, get_db

router = APIRouter(
    prefix=f"{API_PREFIX}/account"
)

def _validate_username(dto: UsernameDto, db: Session):
    user = AccountService.read_account_by_username(db=db, username=dto.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

def _validate_password(dto: PasswordDto, db: Session):
    if dto.password != dto.password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords must match")

def _validate_token(db: Session, token: str):
    if token is None:
        _invalid_token()
    session_id = UUID(f"{{{token}}}")
    valid = SessionService.is_token_valid(db=db, session_id=session_id)
    if valid == False:
        SessionService.delete_session(db=db, session_id=session_id)
        _invalid_token()

def _invalid_token():
    raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
def create_account(dto: AccountCreate, db: Session = Depends(get_db)):
    _validate_username(db=db, dto=dto)
    _validate_password(db=db, dto=dto)
    AccountService.create_account(db=db, account=dto)

@router.get("/", response_model=AccountRead)
def read_account(db: Session = Depends(get_db), token: str | None = Header(default=None)):
    print(token)
    _validate_token(token=token, db=db)
    db_account = SessionService.read_session_bearer(db=db, session_id=token)
    SessionService.update_session(db=db, session_id=token)
    return db_account

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

@router.delete("/")
def delete_account(db: Session = Depends(get_db), token: str | None = Header(default=None)):
    _validate_token(token=token, db=db)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.delete_account(db=db, account_id=account.id)
    SessionService.update_session(db=db, session_id=token)
