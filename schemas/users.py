
from pydantic import BaseModel
from typing import Optional, List




class UserBase(BaseModel):
    name: str
    last_name:  Optional[str] = None
    number: str
    username: str
    roll: str
    password: str



class UserCreate(UserBase):
    pass



class UserUpdate(UserBase):
    id: int
    balance_uzs: float
    balance_usd: float
    status:bool





class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None

class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool