from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from typing import Annotated, List
from models.blog_model import Blog
from schemas.blog_schema import BlogRead, BlogCreate, BlogUpdate, BlogDelete
from config.db_config import get_session
from routers.authenticate import get_current_user, oauth2_scheme
from models.user_model import USER
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def check_admin_user(current_user: USER):
    if not (current_user.is_superuser or current_user.is_staff or current_user.is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )


@router.get("/blogs/{blog_id}", response_model=BlogRead)
async def read_blog(
        blog_id: int,
        session: AsyncSession = Depends(get_session)
) -> BlogRead:
    async with session as sess:
        blog = await sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
    return BlogRead.from_orm(blog)


@router.get("/blogs/", response_model=List[BlogRead])
async def read_blogs(
        session: AsyncSession = Depends(get_session),
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
) -> List[BlogRead]:
    async with session as sess:
        result = await sess.execute(select(Blog).offset(offset).limit(limit))
        blogs = result.scalars().all()
    return [BlogRead.from_orm(blog) for blog in blogs]


@router.post("/blogs/", response_model=BlogRead)
async def create_blog(
        blog: BlogCreate,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> BlogRead:
    current_user = await get_current_user(session=session, token=token)
    check_admin_user(current_user)
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
    return BlogRead.from_orm(db_blog)


@router.put("/blogs/{blog_id}", response_model=BlogRead)
async def update_blog(
        blog_id: int,
        blog: BlogUpdate,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> BlogRead:
    current_user = await get_current_user(session=session, token=token)
    check_admin_user(current_user)
    async with session as sess:
        db_blog = await sess.get(Blog, blog_id)
        if not db_blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        blog_data = blog.model_dump(exclude_unset=True)
        for key, value in blog_data.items():
            setattr(db_blog, key, value)

        sess.add(db_blog)
        await sess.commit()
        await sess.refresh(db_blog)
    return BlogRead.from_orm(db_blog)


@router.delete("/blogs/{blog_id}", response_model=BlogDelete)
async def delete_blog(
        blog_id: int,
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> BlogDelete:
    current_user = await get_current_user(session=session, token=token)
    check_admin_user(current_user)
    async with session as sess:
        blog = await sess.get(Blog, blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        await sess.delete(blog)
        await sess.commit()
    return BlogDelete(ok=True)
