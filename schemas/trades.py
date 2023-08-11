from pydantic import BaseModel


class TradeBase(BaseModel):
    zapchast_id: int
    order_id: int
    quantity:float



class TradeCreate(TradeBase):
    pass


class TradeUpdate(TradeBase):
    id: int
    status: bool
