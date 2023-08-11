from pydantic import BaseModel



class OrderBase(BaseModel):
    customer_id: int



class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: int
    status: bool

