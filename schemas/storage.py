from pydantic import BaseModel


class StorageBase(BaseModel):
    name: str
    birlik: str
    size: str
    number: float
    zapchast_id: int


class StorageCreate(StorageBase):
    pass


class StorageUpdate(StorageBase):
    id: int
    price: float
    currency: str
    status: bool
