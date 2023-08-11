from pydantic import BaseModel
from typing import Optional


class ZapchastBase(BaseModel):
    name: str
    birlik: str
    type_id: int
    size: str
    number: float



class ZapchastCreate(ZapchastBase):
    pass


class ZapchastUpdate(ZapchastBase):
    id: int
    status: bool
