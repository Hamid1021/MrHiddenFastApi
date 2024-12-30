from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from typing import Annotated, List
from models.blog_model import Blog
from schemas.blog_schema import BlogRead, BlogCreate, BlogUpdate
from config.db_config import SessionDep, get_session

router = APIRouter()


@router.post("/blogs/", response_model=BlogRead)
async def create_blog(blog: BlogCreate, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    async with session as sess:
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
        await sess.commit()
        await sess.refresh(db_blog)
    return db_blog


@router.get("/blogs/", response_model=List[BlogRead])
async def read_blogs(
    session: Annotated[SessionDep, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[BlogRead]:
    async with session as sess:
        blogs = await sess.exec(select(Blog).offset(offset).limit(limit))
        return blogs.all()


@router.get("/blogs/{blog_id}", response_model=BlogRead)
async def read_blog(blog_id: int, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    async with session as sess:
        blog = await sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/blogs/{blog_id}", response_model=BlogRead)
async def update_blog(blog_id: int, blog: BlogUpdate, session: Annotated[SessionDep, Depends(get_session)]) -> BlogRead:
    async with session as sess:
        db_blog = await sess.get(Blog, blog_id)
        if not db_blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        blog_data = blog.dict(exclude_unset=True)
        for key, value in blog_data.items():
            setattr(db_blog, key, value)

        sess.add(db_blog)
        await sess.commit()
        await sess.refresh(db_blog)
    return db_blog


@router.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: int, session: Annotated[SessionDep, Depends(get_session)]):
    async with session as sess:
        blog = await sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        await sess.delete(blog)
        await sess.commit()
    return {"ok": True}
