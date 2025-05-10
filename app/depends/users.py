from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.schemas.auth import AccessRefreshTokenResponse
from app.utils.auth import create_token
from app.db.models.users import User
from app.db.database import Base
from app import config


async def register_user(user_obj: Base, db: AsyncSession) -> Base:
    """
    Функция, примающая модель юзера
    И добавляющая ее в сессию бд
    """
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


async def login_user(
    user_data, db: AsyncSession
) -> AccessRefreshTokenResponse | None | str:
    """
    Функция, делающая запрос в бд, где получает юзера по username,
    После чего проверяет пароль и создает токены
    """
    try:
        # TODO: Рассмотреть вариант выделения этой логики в отдельную функцию - authenticate
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user or not user.verify_password(user_data.username):
            return None
        else:
            # TODO: И это тоже выделить в отдельную функцию - что-то типа access_and_refresh_token_response
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
            response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="lax"
            )
            return response
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
