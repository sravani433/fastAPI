# schemas.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    city: str
    isMale: bool

    class Config:
        orm_mode = True

class RegisteredUserCreate(BaseModel):
    name: str
    password: str  # Plain password input

    class Config:
        orm_mode = True

class RegisteredUserResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
