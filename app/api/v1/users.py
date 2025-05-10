from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.users import User
from app.schemas.users import UserRegister
from app.depends.users import register_user
from app.utils.etc import handle_db_result
from app.utils.auth import create_user_model, revoke_token, verify_token

router = APIRouter()


@router.post("/register", status_code=201)
async def register(
    user_data: UserRegister, db: AsyncSession = Depends(get_db)
):
    user_obj = create_user_model(
        user_class=User, user_data=user_data.model_dump()
    )
    result = await register_user(user_obj=user_obj, db=db)
    handle_db_result(result)
    return {"status": "success"}


@router.post("/logout")
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    access_token = request.headers.get("Authorization")
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Нет access токена")
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Нет refresh токена")
    await revoke_token(token=access_token, db=db)
    await revoke_token(token=refresh_token, db=db)
    return {"status": "success"}
