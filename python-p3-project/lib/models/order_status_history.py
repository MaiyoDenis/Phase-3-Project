# lib/models/order_status_history.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class OrderStatusHistory(Base):
    __tablename__ = 'order_status_history'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("Order", back_populates="status_history")
    
    # ORM methods
    @classmethod
    def get_all_by_order(cls, session, order_id):
        return session.query(cls).filter_by(order_id=order_id).order_by(cls.timestamp).all()
    
    def __repr__(self):
        return f"<OrderStatusHistory id={self.id} order_id={self.order_id} status={self.status}>"