import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship

from db import Base




class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    roll = Column(String(20), nullable=True)
    name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    number = Column(String(30), nullable=True)
    balance_uzs = Column(Integer, nullable=True, default=0)
    balance_usd = Column(Integer, nullable=True, default=0)
    username = Column(String(50), unique=True, nullable=True)
    password = Column(String(200), nullable=True)
    status = Column(Boolean, nullable=True, default=True)
    token = Column(String(400), default='', nullable=True)

