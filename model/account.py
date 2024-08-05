from sqlalchemy import Column, Integer, ForeignKey, String

from persistence.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)

class Username(Base):
    __tablename__ = "usernames"

    id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
    username = Column(String, unique=True, index=True)

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
    salt = Column(String)
    password = Column(String)
