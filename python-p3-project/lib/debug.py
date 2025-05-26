# lib/debug.py

import ipdb
from models import Base, engine, Session, Customer, Service, Order, Location, OrderStatusHistory

# Create all tables
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Use ipdb to debug and explore the models
ipdb.set_trace()