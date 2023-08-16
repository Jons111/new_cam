from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Trades(Base):
    __tablename__ = "Trades"
    id = Column(Integer, primary_key=True)
    zapchast_id = Column(Integer, ForeignKey('Zapchasts.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey('Orders.id', ), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    zapchast = relationship("Zapchasts", back_populates="trade")
    order = relationship("Orders", back_populates="trade")
    debt = relationship("Debts", back_populates="trade")
    income = relationship("Incomes", back_populates="trade")
