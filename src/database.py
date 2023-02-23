import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.DATABASE_CONFIG)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
