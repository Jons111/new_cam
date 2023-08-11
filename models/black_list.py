from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Date
from sqlalchemy.orm import relationship, backref

from db import Base
from models.customers import Customers


class Black_list(Base):
    __tablename__ = "Black_list"
    id = Column(Integer, primary_key=True)
    money = Column(Integer, nullable=True)
    customer_id = Column(Integer,ForeignKey("Customers.id"),nullable=False)
    debt_id = Column(Integer,ForeignKey("Debts.id"),nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    deadline = Column(Date,nullable=True)


