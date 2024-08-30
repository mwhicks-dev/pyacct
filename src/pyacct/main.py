import os
import json

import uvicorn

from pyacct_token_validator import PyacctTokenValidator
from persistence.database import Base, engine, SessionLocal
import persistence.session
from persistence.attribute import AttributeService
from api import AccountRouter, SessionRouter

from fastapi import FastAPI, Depends

PYACCT_PORT = os.environ.get("PYACCT_PORT", 8000)

Base.metadata.create_all(bind=engine)

# create all attributes
with open("config/config.json", "r") as fp:
    config = json.load(fp)

for attribute in config['attributes']:
    # TODO: User superuser to set
    AttributeService.update_attribute(db=SessionLocal(),
        key=attribute['key'],
        required=attribute['required'],
        unique=attribute['unique'],
        sensitive=attribute['sensitive']
    )

persistence.session.token_validation = PyacctTokenValidator()

app = FastAPI()
app.include_router(AccountRouter)
app.include_router(SessionRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=PYACCT_PORT, 
                reload=True)