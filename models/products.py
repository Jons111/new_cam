from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Float
from sqlalchemy.orm import relationship

from db import Base


class Products(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type_id = Column(Integer,ForeignKey("Types.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(30), nullable=False)
    user_id = Column(Integer,ForeignKey("Users.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False, default=True)


    type = relationship("Types", back_populates="product")


