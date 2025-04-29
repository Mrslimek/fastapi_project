from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas.users import UserRegister
from depends.users import register_user
from utils.etc import handle_db_result


router = APIRouter()


@router.post("/register", status_code=201)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    result = await register_user(user_data=user_data, db=db)
    handle_db_result(result)
    return {"status": "success"}
