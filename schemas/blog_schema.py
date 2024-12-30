from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BlogCreate(BaseModel):
    title: str
    slug: str
    blog_photo: Optional[str] = None
    short_description: Optional[str] = None
    text: str
    save_type: str
    author: int


class BlogRead(BaseModel):
    id: int
    title: str
    slug: str
    blog_photo: Optional[str] = None
    short_description: Optional[str] = None
    text: str
    save_type: str
    author: int
    created: datetime
    modified: datetime
    is_delete: bool

    class Config:
        from_attributes = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    blog_photo: Optional[str] = None
    short_description: Optional[str] = None
    text: Optional[str] = None
    save_type: Optional[str] = None
    is_delete: Optional[bool] = None

    class Config:
        from_attributes = True
