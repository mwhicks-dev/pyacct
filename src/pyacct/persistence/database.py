import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("config/config.json", "r") as f:
    config = json.load(f)
    engine = create_engine(config['sqlalchemy_url'])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()