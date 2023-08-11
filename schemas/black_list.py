from pydantic import BaseModel


class Black_ListBase(BaseModel):
    money: float
    customer_id: int
    debt_id: int


class Black_ListCreate(Black_ListBase):
    pass


class Black_ListUpdate(Black_ListBase):
    id: int
    status: bool