from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.utils.auth import create_token
from app.db.models.users import User
from app.db.database import Base
from app import config


async def register_user(user_obj: Base, db: AsyncSession) -> Base:
    try:
        async with db.begin():
            db.add(user_obj)
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
    return user_obj


async def login_user(user_data, db: AsyncSession) -> dict | None | str:
    try:
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user or not user.verify_password(user_data.username):
            return None
        else:
            jwt_data = {"sub": user.username}
            access_token = create_token(
                jwt_data=jwt_data,
                expires_delta=timedelta(
                    minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
                ),
            )
            refresh_token = create_token(
                jwt_data=jwt_data,
                expires_delta=timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS),
            )
            # TODO: Доделать создание эндпоинтов для аутентификации
            # Это реализация функции, которая отдает access и refresh токены
            # Надо сделать эндпоинт для обновления access по refresh
            # и эндпоинт для логаута
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
