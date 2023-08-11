from pydantic import BaseModel


class TypeBase(BaseModel):
    name: str


class TypeCreate(TypeBase):
    pass


class TypeUpdate(TypeBase):
    id: int
    status: bool
