# lib/models/__init__.py

from .base import Base, engine, Session
from .customer import Customer
from .service import Service
from .order import Order
from .location import Location
from .order_status_history import OrderStatusHistory

# Create all tables
def create_tables():
    Base.metadata.create_all(engine)