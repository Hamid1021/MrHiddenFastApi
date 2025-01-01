from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Blog(SQLModel, table=True):
    __tablename__ = "Blogs"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str = Field(index=True)
    blog_photo: Optional[str] = Field(default=None)
    short_description: Optional[str] = Field(default=None)
    text: str
    save_type: str = Field(default="N")
    author: Optional[int] = Field(default=None, foreign_key="Users.id")
    created: datetime = Field(default_factory=datetime.utcnow)
    modified: datetime = Field(default_factory=datetime.utcnow)
    is_delete: bool = Field(default=False)
