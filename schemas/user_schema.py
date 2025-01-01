from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseUserCreate(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: str
    gender: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class BaseUser(BaseModel):
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
        from_attributes = True


class UserRead(BaseUser):
    is_active: Optional[bool] = None
    date_joined: Optional[datetime] = None
    last_login: Optional[datetime] = None


class StaffUserRead(UserRead):
    is_staff: Optional[bool] = None


class SuperuserRead(StaffUserRead):
    is_superuser: Optional[bool] = None


class OwnerRead(SuperuserRead):
    is_owner: Optional[bool] = None


class BaseUserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class StaffUserUpdate(BaseUserUpdate):
    is_active: Optional[bool] = None


class SuperuserUpdate(StaffUserUpdate):
    is_superuser: Optional[bool] = None


class OwnerUpdate(SuperuserUpdate):
    is_owner: Optional[bool] = None


class UserDelete(BaseModel):
    ok: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True