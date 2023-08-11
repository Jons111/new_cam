from pydantic import BaseModel


class IncomeBase(BaseModel):
    money: float
    type: str
    currency:str
    customer_id:int
    trade_id:int
    source:str


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(IncomeBase):
    id: int
    status: bool
