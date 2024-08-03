from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session as SQLSession

from schema.session import SessionDto
from schema.account import AccountRead
from model.session import Session, AccountSession
from model.account import Account, Username

class SessionService:

    @staticmethod
    def create_session(db: SQLSession, account_id: int) -> SessionDto:
        t = datetime.now()

        db_session = Session(created_time=t, used_time=t)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        db_join = AccountSession(session_id=db_session.id, account_id=account_id)
        db.add(db_join)
        db.commit()

        return SessionDto(id=db_session.id)
    
    @staticmethod
    def update_session(db: SQLSession, session_id: UUID) -> None:
        t = datetime.now()

        db_session = db.query(Session).filter(Session.id == session_id).first()
        db_session.used_time = t
        db.commit()

        return

    @staticmethod
    def read_session_bearer(db: SQLSession, session_id: UUID) -> AccountRead:
        db_session = db.query(AccountSession).filter(AccountSession.session_id == session_id).first()
        db_account = db.query(Account).filter(Account.id == db_session.account_id).first()
        db_username = db.query(Username).filter(Username.id == db_session.account_id).first()

        return AccountRead(id=db_account.id, username=db_username.username)

    @staticmethod
    def delete_session(db: SQLSession, session_id: UUID) -> None:
        db.query(AccountSession).filter(AccountSession.session_id == session_id).delete()
        db.query(Session).filter(Session.id == session_id).delete()

        return
