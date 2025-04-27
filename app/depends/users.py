from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users.users import UserRegister
from db.models.users import User


async def register_user(user_data: UserRegister, db: AsyncSession):
    # TODO: У UserRegister должна быть проверка на соответствие password и confirm_password
    user_data = user_data.model_dump()
    try:
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
