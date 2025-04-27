from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import get_db
from db.models.users import User
from schemas.users.users import UserLogin, UserRegister
import jwt
from datetime import datetime, timedelta
from depends.users import register_user


router = APIRouter()


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt, decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None


@router.post("/token")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.first_name == user_data.first_name)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not user.verify_password(user_data.password):
        raise HTTPException(status_code=400, detail="Некорректные данные")
    return {"acces_token": create_access_token({"sub": user.first_name})}


@router.post("/register")
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