from pydantic import BaseModel
from typing import List

from schemas.zapchast import ZapchastBaseList


class ProductBase(BaseModel):
    name: str
    type_id: int
    price: float
    currency: str
    zapchast: List[ZapchastBaseList]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int
    status: bool
