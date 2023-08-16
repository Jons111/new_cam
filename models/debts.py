from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float, Date
from sqlalchemy.orm import relationship

from db import Base


class Debts(Base):
    __tablename__ = "Debts"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customers.id"), nullable=False)
    trade_id = Column(Integer, ForeignKey("Trades.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    money = Column(Float, nullable=True)
    currency = Column(String(40), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deadline = Column(Date(), nullable=True)
    status = Column(Boolean, default=True)
    debt_status = Column(Boolean, default=True, nullable=True, )

    customer = relationship("Customers", back_populates="debt")
    trade = relationship("Trades", back_populates="debt")

