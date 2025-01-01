from datetime import datetime

from sqlmodel import Field, SQLModel
from typing import Optional


class USER(SQLModel, table=True):
    __tablename__ = "Users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    password: str = Field(nullable=False)
    pass_per_save: Optional[str] = Field(default=None)
    gender: str = Field(default="m")
    phone_number: Optional[str] = Field(default=None, index=True, unique=True)
    bio: Optional[str] = Field(default=None)
    custom_user_id: Optional[str] = Field(
        default=None, index=True, unique=True)
    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)
    is_staff: Optional[bool] = Field(default=False)
    date_joined: Optional[datetime] = Field(default=datetime.now())
    last_login: Optional[datetime] = Field(default=None)
    is_owner: Optional[bool] = Field(default=False)
