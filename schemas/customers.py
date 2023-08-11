from typing import List, Optional

from pydantic import BaseModel
from schemas.phones import PhoneBase, PhoneUpdateCustomer


class CustomerBase(BaseModel):
    name: str
    last_name: Optional[str] = ''


class CustomerCreate(CustomerBase):
    customer_phones: List[PhoneBase]


class CustomerUpdate(CustomerBase):
    customer_phones: List[PhoneUpdateCustomer]
    id: int
    status: bool



