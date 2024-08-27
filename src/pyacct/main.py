import os

import uvicorn

from pyacct_token_validator import PyacctTokenValidator
from persistence.database import Base, engine
import persistence.session
from api import AccountRouter, SessionRouter

from fastapi import FastAPI

PYACCT_PORT = os.environ.get("PYACCT_PORT", 8000)

Base.metadata.create_all(bind=engine)

persistence.session.token_validation = PyacctTokenValidator()

app = FastAPI()
app.include_router(AccountRouter)
app.include_router(SessionRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", 
                host="127.0.0.1", 
                port=PYACCT_PORT, 
                reload=True)