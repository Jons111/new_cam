from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, and_,Float
from sqlalchemy.orm import relationship

from db import Base



class Types(Base):
    __tablename__ = "Types"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    product = relationship("Products", back_populates="type")
    zapchast = relationship("Zapchasts", back_populates="type")



