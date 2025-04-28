from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.users import UserRegister, UserLogin
from db.models.users import User
from utils.auth import create_access_token


async def register_user(user_data: UserRegister, db: AsyncSession):
    user_data = user_data.model_dump()
    try:
        # TODO: Рассмотреть вариант выноса этой логики в отдельную функцию
        user_password = user_data.pop("password")
        user = User(first_name=user_data["first_name"])
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


async def login_user(user_data: UserLogin, db: AsyncSession) -> dict | None:
    user_data = user_data.model_dump()
    print(user_data)
    try:
        stmt = select(User).where(User.first_name == user_data["first_name"])
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user or not user.verify_password(user_data["password"]):
            return None
        else:
            jwt_data = {"sub": user.first_name}
            return {"access_token": create_access_token(jwt_data)}
    except IntegrityError:
        return "IntegrityError"
    except TypeError:
        return "TypeError"
    except InvalidRequestError:
        return "InvalidRequestError"
