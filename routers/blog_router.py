from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from typing import Annotated, List
from models.blog_model import Blog
from schemas.blog_schema import BlogRead, BlogCreate, BlogUpdate
from config.db_config import SessionDep, get_session

router = APIRouter()

@router.post("/blogs/", response_model=BlogRead)
def create_blog(blog: BlogCreate, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    with session as sess:
        db_blog = Blog(
            title=blog.title,
            slug=blog.slug,
            blog_photo=blog.blog_photo,
            short_description=blog.short_description,
            text=blog.text,
            save_type=blog.save_type,
            author=blog.author,
        )
        sess.add(db_blog)
        sess.commit()
        sess.refresh(db_blog)
    return db_blog

@router.get("/blogs/", response_model=List[BlogRead])
def read_blogs(
    session: Annotated[SessionDep, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[BlogRead]:
    with session as sess:
        blogs = sess.exec(select(Blog).offset(offset).limit(limit)).all()
    return blogs

@router.get("/blogs/{blog_id}", response_model=BlogRead)
def read_blog(blog_id: int, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    with session as sess:
        blog = sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/blogs/{blog_id}", response_model=BlogRead)
def update_blog(blog_id: int, blog: BlogUpdate, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    with session as sess:
        db_blog = sess.get(Blog, blog_id)
        if not db_blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        blog_data = blog.dict(exclude_unset=True)
        for key, value in blog_data.items():
            setattr(db_blog, key, value)

        sess.add(db_blog)
        sess.commit()
        sess.refresh(db_blog)
    return db_blog

@router.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, session: Annotated[SessionDep, Depends(get_session)]):
    with session as sess:
        blog = sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        sess.delete(blog)
        sess.commit()
    return {"ok": True}
