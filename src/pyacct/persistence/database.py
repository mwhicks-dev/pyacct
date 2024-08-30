import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("config/config.json", "r") as fp:
    _config = json.load(fp)

try:
    DATABASE_URL = _config['sqlalchemy_url']
except KeyError:
    raise Exception("Configuration of sqlalchemy_url is required")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()