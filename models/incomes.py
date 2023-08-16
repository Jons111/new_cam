from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float
from sqlalchemy.orm import relationship

from db import Base



class Incomes(Base):
    __tablename__ = "Incomes"
    id = Column(Integer, primary_key=True)
    money = Column(Float, nullable=False)
    customer_id = Column(Integer,ForeignKey("Customers.id"), nullable=False)
    trade_id = Column(Integer,ForeignKey("Trades.id"), nullable=False)
    type = Column(String(20),nullable=True)
    currency = Column(String(20),nullable=True)
    source = Column(String(50),nullable=False)
    user_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    customer = relationship("Customers", back_populates="income")
    trade = relationship("Trades", back_populates="income")

