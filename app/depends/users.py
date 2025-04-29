from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.users import UserRegister
from db.models.users import User
from utils.auth import create_access_token
from schemas.auth import Token


async def register_user(user_data: UserRegister, db: AsyncSession):
    user_data = user_data.model_dump()
    try:
        # TODO: Рассмотреть вариант выноса этой логики в отдельную функцию
        user_password = user_data.pop("password")
        user = User(username=user_data["username"])
        user.set_password(password=user_password)
        async with db.begin():
            db.add(user)
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
    return user


async def login_user(user_data, db: AsyncSession) -> Token | None | str:
    try:
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user or not user.verify_password(user_data.username):
            return None
        else:
            jwt_data = {"sub": user.username}
            access_token = create_access_token(jwt_data)
            return Token(access_token=access_token, token_type="bearer")
            return Token
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
