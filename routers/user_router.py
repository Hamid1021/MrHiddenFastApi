import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Sequence, Type
from sqlmodel import select
from models.user_model import USER
from schemas.user_schema import UserRead, UserCreate, BaseUserUpdate, StaffUserUpdate, SuperuserUpdate, OwnerUpdate
from config.db_config import get_session
from routers.authenticate import oauth2_scheme, get_password_hash, get_current_user
import uuid

router = APIRouter()


async def update_user_helper(user_id: int, user_data: dict, session: AsyncSession) -> Type[USER]:
    async with session as sess:
        db_user = await sess.get(USER, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user_data.items():
            setattr(db_user, key, value)
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


def check_access_level(current_user: USER, target_user: Type[USER]):
    if current_user.is_owner:
        return True
    if current_user.is_superuser and not target_user.is_owner:
        return True
    if current_user.is_staff and not (target_user.is_owner or target_user.is_superuser):
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to modify this user"
    )


async def get_and_check_user(user_id: int, current_user: USER, session: AsyncSession) -> Type[USER] | None:
    async with session as sess:
        db_user = await sess.get(USER, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        check_access_level(current_user, db_user)
    return db_user


async def check_username_exists(username: str, session: AsyncSession):
    async with session as sess:
        result = await sess.execute(select(USER).where(USER.username == username))
        user = result.scalars().first()
        if user:
            raise HTTPException(status_code=400, detail="Username already taken")


@router.post("/users/", response_model=UserRead)
async def create_user(
        user: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    await check_username_exists(user.username, session)
    hashed_password = get_password_hash(user.password)
    async with session as sess:
        db_user = USER(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            pass_per_save=user.password,
            gender=user.gender,
            phone_number=user.phone_number,
            bio=user.bio,
            custom_user_id=str(uuid.uuid4())[:11:-1],
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.datetime.now(),
            is_owner=False,
        )
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


@router.post("/staffusers/", response_model=UserRead)
async def create_staffuser(
        user: UserCreate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> UserRead:
    current_user = await get_current_user(session=session, token=token)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create staff users"
        )
    await check_username_exists(user.username, session)
    hashed_password = get_password_hash(user.password)
    async with session as sess:
        db_user = USER(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            pass_per_save=user.password,
            gender=user.gender,
            phone_number=user.phone_number,
            bio=user.bio,
            custom_user_id=str(uuid.uuid4())[:11:-1],
            is_active=True,
            is_superuser=False,
            is_staff=True,
            date_joined=datetime.datetime.now(),
            is_owner=False,
        )
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


@router.post("/superusers/", response_model=UserRead)
async def create_superuser(
        user: UserCreate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> UserRead:
    current_user = await get_current_user(session=session, token=token)
    if not current_user.is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can create superusers"
        )
    await check_username_exists(user.username, session)
    hashed_password = get_password_hash(user.password)
    async with session as sess:
        db_user = USER(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            pass_per_save=user.password,
            gender=user.gender,
            phone_number=user.phone_number,
            bio=user.bio,
            custom_user_id=str(uuid.uuid4())[:11:-1],
            is_active=True,
            is_superuser=True,
            is_staff=True,
            date_joined=datetime.datetime.now(),
            is_owner=False,
        )
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
    return db_user


@router.get("/users/", response_model=List[UserRead])
async def read_users(
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme),
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[USER]:
    current_user = await get_current_user(session=session, token=token)
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view users"
        )
    async with session as sess:
        result = await sess.execute(select(USER).offset(offset).limit(limit))
        users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(
        user_id: int, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> Type[USER] | None:
    current_user = await get_current_user(session=session, token=token)
    user = await get_and_check_user(user_id, current_user, session)
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
        user_id: int, user: BaseUserUpdate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> Type[USER] | None:
    current_user = await get_current_user(session=session, token=token)
    db_user = await get_and_check_user(user_id, current_user, session)
    user_data = user.dict(exclude_unset=True)
    return await update_user_helper(user_id, user_data, session)


@router.put("/staffusers/{user_id}", response_model=UserRead)
async def update_staffuser(
        user_id: int, user: StaffUserUpdate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> Type[USER] | None:
    current_user = await get_current_user(session=session, token=token)
    db_user = await get_and_check_user(user_id, current_user, session)
    user_data = user.dict(exclude_unset=True)
    return await update_user_helper(user_id, user_data, session)


@router.put("/superusers/{user_id}", response_model=UserRead)
async def update_superuser(
        user_id: int, user: SuperuserUpdate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> Type[USER] | None:
    current_user = await get_current_user(session=session, token=token)
    db_user = await get_and_check_user(user_id, current_user, session)
    user_data = user.dict(exclude_unset=True)
    return await update_user_helper(user_id, user_data, session)


@router.put("/owners/{user_id}", response_model=UserRead)
async def update_owner(
        user_id: int, user: OwnerUpdate, session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme)
) -> Type[USER] | None:
    current_user = await get_current_user(session=session, token=token)
    db_user = await get_and_check_user(user_id, current_user, session)
    user_data = user.dict(exclude_unset=True)
    return await update_user_helper(user_id, user_data, session)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session),
                      token: str = Depends(oauth2_scheme)):
    current_user = await get_current_user(session=session, token=token)
    async with session as sess:
        user = await sess.get(USER, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not (current_user.is_superuser or current_user.is_owner):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only superusers and owners can delete users"
            )
        check_access_level(current_user, user)
        await sess.delete(user)
        await sess.commit()
    return {"ok": True}
