import os
import json

import uvicorn

from pyacct_token_validator import PyacctTokenValidator
from persistence.database import Base, engine
import persistence.session
from api import AccountRouter, SessionRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PYACCT_PORT = os.environ.get("PYACCT_PORT", 8000)

Base.metadata.create_all(bind=engine)

persistence.session.token_validation = PyacctTokenValidator()

app = FastAPI()
app.include_router(AccountRouter)
app.include_router(SessionRouter)

with open("config/cors.json", "r") as f:
    origins = json.load(f)['origins']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=PYACCT_PORT, 
                reload=True)