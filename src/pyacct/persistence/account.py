from sqlalchemy.orm import Session as SQLSession

from model import Account, Username, Password, Attribute
from schema import AccountCreate, AccountRead, UsernameDto, PasswordDto
from util import PasswordHash

class AccountService:

    @staticmethod
    def create_account(db: SQLSession, account: AccountCreate) -> None:
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

        # store attributes
        for attribute in account.attributes:
            db_attribute = Attribute(account_id=db_account.id,
                                     key=attribute.key,
                                     value=attribute.value)
            db.add(db_attribute)
            db.commit()

        return
    
    @staticmethod
    def read_account(db: SQLSession, account_id: int) -> AccountRead:
        account = db.query(Account).filter(Account.id == account_id).first()
        username = db.query(Username).filter(Username.id == account_id).first()

        return AccountRead(id=account.id, username=username.username)
    
    @staticmethod
    def read_account_by_username(db: SQLSession, username: str) -> AccountRead:
        account = db.query(Username).filter(Username.username == username).first()

        if account is None:
            return None

        return AccountRead(id=account.id, username=account.username)
    
    @staticmethod
    def read_account_by_unique_attribute(db: SQLSession, key: str, value: str) -> AccountRead:
        attribute = db.query(Attribute).filter(Attribute.key == key).filter(
            Attribute.value == value).first()
        
        if attribute is None:
            return None
        
        return AccountService.read_account(db=db, account_id=attribute.account_id)
    
    @staticmethod
    def read_password(db: SQLSession, account_id: int) -> Password:
        return db.query(Password).filter(Password.id == account_id).first()

    @staticmethod
    def update_username(db: SQLSession, account_id: int, dto: UsernameDto) -> None:
        username = db.query(Username).filter(Username.id == account_id).first()
        username.username = dto.username
        db.commit()

        return

    @staticmethod
    def update_password(db: SQLSession, account_id: int, dto: PasswordDto) -> None:
        password = db.query(Password).filter(Password.id == account_id).first()
        hashed_password = PasswordHash.hash_password(dto.password)
        password.salt = hashed_password.salt
        password.password = hashed_password.password
        db.commit()

        return
    
    @staticmethod
    def delete_account(db: SQLSession, account_id: int) -> None:
        db.query(Username).filter(Username.id == account_id).delete()
        db.query(Password).filter(Password.id == account_id).delete()
        db.query(Attribute).filter(Attribute.account_id == account_id).delete()
        db.query(Account).filter(Account.id == account_id).delete()
        db.commit()
