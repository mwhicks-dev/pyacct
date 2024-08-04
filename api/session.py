from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session as SQLSession

from util.password_hash import PasswordHash
from schema.session import SessionCreate, SessionDto
from persistence.account import AccountService
from persistence.session import SessionService
from api.api import API_PREFIX, get_db

router = APIRouter(
    prefix=f"{API_PREFIX}/session"
)

@router.post("/")
def create_session(dto: SessionCreate, db: SQLSession = Depends(get_db)):
    # get account details by username
    db_account = AccountService.read_account_by_username(db=db, username=dto.username)
    if db_account is None:
        _bad_credentials()
    challenge = AccountService.read_password(db=db, account_id=db_account.id)
    if challenge is None:
        _bad_credentials()
    
    # hash password based on salt
    response = PasswordHash.hash_password(password=dto.password, salt=challenge.salt)

    # check for match
    if response.password != challenge.password:
        _bad_credentials()
    
    # create new session
    session = SessionService.create_session(db=db, account_id=db_account.id)

    # ref: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
    return {"access_token" : str(session.id), "token_type" : "bearer"}

def _bad_credentials():
    raise HTTPException(status_code=401, detail="Invalid credentials")