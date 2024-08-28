import os
import json

from pyacct_token_validator import PyacctTokenValidator
from persistence.database import Base, engine
import persistence.session
from api import AccountRouter, SessionRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

persistence.session.token_validation = PyacctTokenValidator()

app = FastAPI()
app.include_router(AccountRouter)
app.include_router(SessionRouter)

# set configuration variables
with open("config/config.json", "r") as f:
    config = json.load(f)

os.environ['PYACCT_DATABASE_URL'] = config['sqlalchemy_url']

app.add_middleware(
    CORSMiddleware,
    allow_origins=config['origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)