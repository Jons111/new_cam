from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Storage(Base):
    __tablename__ = "Storage"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birlik = Column(String(20), nullable=False)
    zapchast_id = Column(Integer,ForeignKey("Zapchasts.id"), nullable=False)
    size = Column(String(50), nullable=True)
    number = Column(Float, nullable=True)
    price = Column(Integer, nullable=True)
    currency = Column(String(30), nullable=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)




