from sqlalchemy import Column, Integer, String, DateTime, Boolean, func,Float,ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Customers(Base):
    __tablename__ = "Customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    debt_uzs = Column(Float, nullable=False,default=0)
    debt_usd = Column(Float, nullable=False,default=0)
    user_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    phone = relationship("Phones", back_populates="customer")
    debt= relationship("Debts", back_populates="customer")
    order= relationship("Orders", back_populates="customer")
    income= relationship("Incomes", back_populates="customer")


