from pydantic import BaseModel


class RefreshToken(BaseModel):
    """
    Схема для валидации refresh токена
    """
    refresh_token: str


class AccessTokenResponse(BaseModel):
    """
    Схема для валидации access токена
    """
    access_token: str
    token_type: str


class AccessRefreshTokenResponse(BaseModel):
    """
    Схема для валидации словаря с
    access и refresh токеном
    """
    access_token: str
    refresh_token: str
    grant_type: str
