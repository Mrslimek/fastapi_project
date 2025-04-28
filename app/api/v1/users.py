from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas.users import UserLogin, UserRegister
from depends.users import register_user, login_user


router = APIRouter()


@router.post("/token")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await login_user(user_data=user_data, db=db)
    match result:
        case None:
            raise HTTPException(status_code=404, detail="Неверные имя пользователя или пароль")
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный тип данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
    return result


@router.post("/register", status_code=201)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await register_user(user_data=user_data, db=db)
    match result:
        case "IntegrityError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
        case "TypeError":
            raise HTTPException(status_code=400, detail="Неверный тип данных")
        case "InvalidRequestError":
            raise HTTPException(status_code=400, detail="Некорректные данные")
    return {"status": "success"}