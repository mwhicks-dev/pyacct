from sqlalchemy.orm import Session

from model.account import Account, Username, Password
from schema.account import AccountCreate, AccountRead, UsernameDto, PasswordDto
from model.session import AccountSession, Session
from util.password_hash import PasswordHash

class AccountService:

    @staticmethod
    def create_account(db: Session, account: AccountCreate) -> None:
        # generate ID
        db_account = Account()
        db.add(db_account)
        db.commit()
        db.refresh(db_account)

        # store username and password
        db_username = Username(id=db_account.id, username=account.username)
        db_password = PasswordHash.hash_password(account.password)
        db_password.id = db_account.id
        db.add(db_username)
        db.add(db_password)
        db.commit()

        return
    
    @staticmethod
    def read_account(db: Session, account_id: int) -> AccountRead:
        account = db.query(Account).filter(Account.id == account_id).first()
        username = db.query(Username).filter(Username.id == account_id).first()

        return AccountRead(id=account.id, username=username.username)

    @staticmethod
    def update_username(db: Session, account_id: int, dto: UsernameDto) -> None:
        username = db.query(Username).filter(Username.id == account_id).first()
        username.username = dto.username
        db.commit()

        return

    @staticmethod
    def update_password(db: Session, account_id: int, dto: PasswordDto) -> None:
        password = db.query(Password).filter(Password.id == account_id).first()
        hashed_password = PasswordHash.hash_password(dto.password)
        password.salt = hashed_password.salt
        password.password = hashed_password.password
        db.commit()

        return
    
    @staticmethod
    def delete_account(db: Session, account_id: int) -> None:
        session_id = db.query(AccountSession).filter(AccountSession.account_id == account_id).first()
        if session_id is not None:
            db.query(AccountSession).filter(AccountSession.session_id == session_id).delete()
            db.query(Session).filter(Session.id == session_id).delete()
        db.query(Username).filter_by(Username.id == account_id).delete()
        db.query(Password).filter_by(Password.id == account_id).delete()
        db.query(Account).filter_by(Account.id == account_id).delete()
