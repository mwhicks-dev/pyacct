from sqlalchemy import Column, ForeignKey, Uuid, DateTime, Integer, PrimaryKeyConstraint

from persistence.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Uuid, primary_key=True)
    created_time = Column(DateTime)
    used_time = Column(DateTime)

class AccountSession(Base):
    __tablename__ = "account_sessions"

    session_id = Column(Uuid, ForeignKey("sessions.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))

    # ref: https://stackoverflow.com/questions/10059345/sqlalchemy-unique-across-multiple-columns
    __table_args__ = (PrimaryKeyConstraint("session_id", "account_id"), )
