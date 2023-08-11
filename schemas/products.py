from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    type_id: int
    price: float
    currency:str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int
    status: bool
