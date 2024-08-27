from fastapi.security import OAuth2PasswordBearer

from persistence.database import SessionLocal

API_PREFIX = "/pyacct/1"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
