from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from datetime import datetime, timedelta
import jwt
from app.db.database import get_db, Base
from app.db.models.users import User
from app.db.models.auth import RevokedToken
from app import config
from typing import Type

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(jwt_data: dict, expires_delta: timedelta):
    to_encode = jwt_data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def verify_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    revoked_token = await is_token_revoked(token=token, db=db)
    if revoked_token:
        raise jwt.ExpiredSignatureError
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    async with db.begin():
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        user = result.scalars().first()
    return user


def create_user_model(user_class: Type[Base], user_data: dict):
    user_password = user_data.pop("password")
    user = User(username=user_data["username"])
    user.set_password(password=user_password)
    return user


def get_refresh_token_from_cookies(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Нет refresh токена")
    return refresh_token


def decode_jwt_token(
    token: str, secret_key: str, algorithm: str
) -> dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Нет username"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
        )


async def get_user_from_db(
    username: str, user_class: Type[Base], db: AsyncSession
) -> Base:
    stmt = select(user_class).where(user_class.username == username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user


async def revoke_token(token: str, db: AsyncSession):
    async with db.begin():
        await db.execute(insert(RevokedToken).values(token=token))


async def is_token_revoked(token: str, db: AsyncSession):
    async with db.begin():
        result = await db.execute(
            select(RevokedToken).where(RevokedToken.token == token)
        )
        return result.scalars().first()
