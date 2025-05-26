# lib/models/base.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a base class for our models
Base = declarative_base()

# Create engine and session
engine = create_engine('sqlite:///laundry_connect.db')
Session = sessionmaker(bind=engine)