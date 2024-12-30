from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: str
    pass_per_save: Optional[str] = None
    gender: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    custom_user_id: Optional[str] = None


class UserRead(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
