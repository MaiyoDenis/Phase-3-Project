# lib/models/order.py

from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from .base import Base
from .order_status_history import OrderStatusHistory
from .service import Service

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    weight = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default='placed')
    pickup_date = Column(Date, nullable=False)
    pickup_time = Column(String, nullable=False)  # 'morning', 'afternoon', 'evening'
    special_instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    service = relationship("Service", back_populates="orders")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")
    
    # Property methods
    @property
    def weight(self):
        return self._weight
        
    @weight.setter
    def weight(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Weight must be a positive number")
        self._weight = value
    
    @property
    def pickup_date(self):
        return self._pickup_date
        
    @pickup_date.setter
    def pickup_date(self, value):
        # Ensure pickup date is not in the past
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        
        if value < date.today():
            raise ValueError("Pickup date cannot be in the past")
        
        self._pickup_date = value
    
    # ORM methods
    @classmethod
    def create(cls, session, customer_id, service_id, weight, pickup_date, pickup_time, special_instructions=None):
        # Calculate total price based on service price and weight
        service = session.query(Service).filter_by(id=service_id).first()
        if not service:
            raise ValueError("Invalid service ID")
        
        total_price = service.price_per_unit * weight
        
        # Create order
        order = cls(
            customer_id=customer_id,
            service_id=service_id,
            weight=weight,
            total_price=total_price,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            special_instructions=special_instructions,
            status='placed'
        )
        
        session.add(order)
        session.flush()  # Flush to get the order ID
        
        # Create initial status history entry
        history_entry = OrderStatusHistory(
            order_id=order.id,
            status='placed',
            timestamp=datetime.utcnow()
        )
        
        session.add(history_entry)
        session.commit()
        return order
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_customer(cls, session, customer_id):
        return session.query(cls).filter_by(customer_id=customer_id).all()
    
    @classmethod
    def find_by_status(cls, session, status):
        return session.query(cls).filter_by(status=status).all()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        order = cls.find_by_id(session, id)
        if not order:
            return None
        
        # Special handling for status updates
        if 'status' in kwargs and kwargs['status'] != order.status:
            # Create status history entry
            history_entry = OrderStatusHistory(
                order_id=order.id,
                status=kwargs['status'],
                timestamp=datetime.utcnow()
            )
            session.add(history_entry)
        
        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)
        
        session.commit()
        return order
    
    @classmethod
    def delete(cls, session, id):
        order = cls.find_by_id(session, id)
        if not order:
            return False
        
        session.delete(order)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Order id={self.id} customer_id={self.customer_id} status={self.status}>"