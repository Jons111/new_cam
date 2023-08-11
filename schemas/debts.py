from pydantic import BaseModel
from typing import Optional
from pydantic.datetime_parse import date


class DebtBase(BaseModel):
    money: float
    customer_id: int
    trade_id: int
    currency: str
    deadline: date


class DebtCreate(DebtBase):
    pass


class DebtUpdate(DebtBase):
    id: int
    status: bool
    debt_status: bool
