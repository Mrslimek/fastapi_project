from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.db.database import get_db
from app.db.models.users import User
from app.depends.users import login_user
from app.utils.etc import handle_db_result
from app.utils.auth import (
    get_refresh_token_from_cookies,
    decode_jwt_token,
    get_user_from_db,
    create_token,
)
from app.schemas.auth import AccessTokenResponse
from app import config


router = APIRouter()


@router.post("/token")
async def token(
    user_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    response = await login_user(user_data=user_data, db=db)
    handle_db_result(response)
    return response


@router.post("/token/refresh", response_model=AccessTokenResponse)
async def refresh_access_token(
    request: Request, db: AsyncSession = Depends(get_db)
) -> AccessTokenResponse:
    refresh_token = get_refresh_token_from_cookies(request=request)
    payload = decode_jwt_token(
        token=refresh_token,
        secret_key=config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )
    user = await get_user_from_db(
        username=payload.get("sub"), user_class=User, db=db
    )
    if not user:
        raise HTTPException(status_code=400, detail="Нет такого юзера")
    else:
        new_access_token = create_token(
            jwt_data={"sub": user.username},
            expires_delta=timedelta(days=config.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        response = {
            "access_token": new_access_token,
            "token_type": "bearer",
        }
        return response
