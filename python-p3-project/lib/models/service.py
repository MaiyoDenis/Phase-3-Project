# lib/models/service.py

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # 'kg' or 'item'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="service")
    
    # Property methods
    @property
    def price_per_unit(self):
        return self._price_per_unit
        
    @price_per_unit.setter
    def price_per_unit(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price_per_unit = value
    
    # ORM methods
    @classmethod
    def create(cls, session, name, price_per_unit, unit, description=None):
        service = cls(name=name, price_per_unit=price_per_unit, unit=unit, description=description)
        session.add(service)
        session.commit()
        return service
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        service = cls.find_by_id(session, id)
        if not service:
            return None
        
        for key, value in kwargs.items():
            if hasattr(service, key):
                setattr(service, key, value)
        
        session.commit()
        return service
    
    @classmethod
    def delete(cls, session, id):
        service = cls.find_by_id(session, id)
        if not service:
            return False
        
        session.delete(service)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Service id={self.id} name={self.name} price={self.price_per_unit}/{self.unit}>"