from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from schema.account import AccountCreate, AccountRead, UsernameDto, PasswordDto
from persistence.account import AccountService
from persistence.session import SessionService
from api.api import API_PREFIX, get_db, oauth2_scheme

router = APIRouter(
    prefix=f"{API_PREFIX}/account"
)

def _validate_username(dto: UsernameDto, db: Session = Depends(get_db)):
    user = AccountService.read_account_by_username(db=db, username=dto.username)
    if user is not None:
        raise HTTPException(status_code=400, detail="Username already taken")

def _validate_password(dto: PasswordDto, db: Session = Depends(get_db)):
    if dto.password != dto.password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords must match")

@router.post("/")
def create_account(dto: AccountCreate, db: Session = Depends(get_db)):
    _validate_username(dto)
    _validate_password(dto)
    AccountService.create_account(db=db, account=dto)

@router.get("/", response_model=AccountRead)
def read_account(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return SessionService.read_session_bearer(db=db, session_id=token)

@router.put("/username")
def update_username(dto: UsernameDto, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    _validate_username(dto)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.update_username(db=db, account_id=account.id, dto=dto)

@router.put("/password")
def update_password(dto: PasswordDto, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    _validate_password(dto)
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.update_password(db=db, account_id=account.id, dto=dto)

@router.delete("/")
def delete_account(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    account = SessionService.read_session_bearer(db=db, session_id=token)
    AccountService.delete_account(db=db, account_id=account.id)
