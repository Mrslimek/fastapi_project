from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.depends.users import login_user
from app.schemas.auth import Token


router = APIRouter()


@router.post("/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Token:
    result = await login_user(user_data=form_data, db=db)
    match result:
        case None:
            raise HTTPException(
                status_code=404, detail="Неверные имя пользователя или пароль"
            )
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный тип данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
    return result
