from typing import Any
import json

from pyacct_token_validator import PyacctTokenValidator
from persistence.database import Base, engine, SessionLocal
import persistence.session
from persistence.attribute import AttributeService
from api import AccountRouter, SessionRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

# create all attributes
with open("config/config.json", "r") as fp:
    config: dict[str, Any] = json.load(fp)

for attribute in config.get('attributes', []):
    AttributeService.update_attribute(db=SessionLocal(),
        key=attribute['key'],
        required=attribute['required'],
        unique=attribute['unique'],
        sensitive=attribute['sensitive']
    )

persistence.session.token_validation = PyacctTokenValidator()
if config.get('generate_docs', False):
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(AccountRouter)
app.include_router(SessionRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config['origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)