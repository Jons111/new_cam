from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Zapchasts(Base):
    __tablename__ = "Zapchasts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birlik = Column(String(20), nullable=False)
    type_id = Column(Integer, ForeignKey("Types.id"), nullable=False)
    size = Column(String(50), nullable=True)
    number = Column(Float, nullable=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    type = relationship("Types", back_populates="zapchast")
    trade = relationship("Trades", back_populates="zapchast")
    storage = relationship("Storage", back_populates="zapchast")
