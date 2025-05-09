from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.users import User
from app.schemas.users import UserRegister
from app.depends.users import register_user
from app.utils.etc import handle_db_result
from app.utils.auth import create_user_model

router = APIRouter()


@router.post("/register", status_code=201)
async def register(
    user_data: UserRegister, db: AsyncSession = Depends(get_db)
):
    user_obj = create_user_model(user_class=User, user_data=user_data.model_dump())
    result = await register_user(user_obj=user_obj, db=db)
    handle_db_result(result)
    return {"status": "success"}
