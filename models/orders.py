import uuid

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_, Identity, Float, Date
from sqlalchemy.orm import relationship, backref

import db
from db import Base
from models.customers import Customers


class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True, )
    savdo_id = Column(Integer, nullable=True,default=0 )
    customer_id = Column(Integer, ForeignKey('Customers.id'), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    type = Column(String(20), nullable=True, )
    currency = Column(String(20), nullable=True, )
    order_status = Column(String(30), nullable=True)
    summ = Column(Float, nullable=True, default=0)
    rest_summ = Column(Float, nullable=True, default=0)
    discount = Column(Float, nullable=True, default=0)
    real_summ = Column(Float, nullable=True, default=0)
    payment_summ = Column(Float, nullable=True, default=0)


    customer = relationship("Customers", back_populates="order")
    trade = relationship("Trades", back_populates="order")




