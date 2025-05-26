# lib/models/customer.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import re

from .base import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    
    # Property methods for validation
    @property
    def phone(self):
        return self._phone
        
    @phone.setter
    def phone(self, value):
        # Validate phone number (simple validation for Kenyan numbers)
        if not value:
            raise ValueError("Phone number cannot be empty")
        
        # Remove any non-digit characters
        phone_digits = re.sub(r'\D', '', value)
        
        # Kenyan numbers are typically 9-10 digits
        if len(phone_digits) < 9 or len(phone_digits) > 12:
            raise ValueError("Invalid phone number length")
            
        self._phone = value
    
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Name must be at least 3 characters")
        self._name = value
    
    # ORM methods
    @classmethod
    def create(cls, session, name, phone, email=None, address=None):
        customer = cls(name=name, phone=phone, email=email, address=address)
        session.add(customer)
        session.commit()
        return customer
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_phone(cls, session, phone):
        return session.query(cls).filter_by(phone=phone).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        customer = cls.find_by_id(session, id)
        if not customer:
            return None
        
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        
        session.commit()
        return customer
    
    @classmethod
    def delete(cls, session, id):
        customer = cls.find_by_id(session, id)
        if not customer:
            return False
        
        session.delete(customer)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Customer id={self.id} name={self.name} phone={self.phone}>"