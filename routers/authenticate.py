from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlmodel import select
from passlib.context import CryptContext
from config.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import USER
from schemas.authenticate_schema import AuthenticateRead, AuthenticateCreate

router = APIRouter()

SECRET_KEY = 'a1e0a73ecac6e1d5c1a3005040587fa119b02239f1268d0ca2355a7c4c4e984c'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate/gettoken/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def verify_user_credentials(username: str, password: str, session: AsyncSession):
    async with session as sess:
        result = await sess.execute(select(USER).where(USER.username == username))
        user = result.scalars().first()
    if user and verify_password(password, user.password):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> USER:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    async with session as sess:
        result = await sess.execute(select(USER).where(USER.username == username))
        user = result.scalars().first()
        if user is None:
            raise credentials_exception
        return user


@router.post("/authenticate/gettoken/", response_model=AuthenticateRead)
async def login(
        form_data: AuthenticateCreate,
        session: AsyncSession = Depends(get_session)
) -> AuthenticateRead:
    user = await verify_user_credentials(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_owner": user.is_owner
        },
        expires_delta=access_token_expires
    )

    async with session as sess:
        user.last_login = datetime.utcnow()
        sess.add(user)
        await sess.commit()
        await sess.refresh(user)

    return AuthenticateRead(access_token=access_token, token_type="bearer")
