from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from typing import Annotated, List
from models.user_model import USER
from schemas.user_schema import UserRead, UserCreate, UserUpdate
from config.db_config import SessionDep, get_session

router = APIRouter()


@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: Annotated[SessionDep, Depends(get_session)]) -> UserRead:
    async with session as sess:
        db_user = USER(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            pass_per_save=user.pass_per_save,
            gender=user.gender,
            phone_number=user.phone_number,
            bio=user.bio,
            custom_user_id=user.custom_user_id,
        )
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[UserRead])
async def read_users(
    session: Annotated[SessionDep, Depends(get_session)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[UserRead]:
    async with session as sess:
        result = await sess.execute(select(USER).offset(offset).limit(limit))
        users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: Annotated[SessionDep, Depends(get_session)]) -> UserRead:
    async with session as sess:
        user = await sess.get(USER, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, session: Annotated[SessionDep, Depends(get_session)]) -> UserRead:
    async with session as sess:
        db_user = await sess.get(USER, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)

        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: Annotated[SessionDep, Depends(get_session)]):
    async with session as sess:
        user = await sess.get(USER, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await sess.delete(user)
        await sess.commit()
    return {"ok": True}
