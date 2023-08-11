
from pydantic import BaseModel
from typing import Optional


class PhoneBase(BaseModel):
    number: str


class PhoneCreate(PhoneBase):
    source_id: int


class PhoneUpdate(PhoneBase):
    id: int
    source_id: int

class PhoneUpdateCustomer(PhoneBase):
    id: int

