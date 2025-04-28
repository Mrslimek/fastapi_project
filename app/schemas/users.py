from pydantic import BaseModel


class UserLogin(BaseModel):
    first_name: str
    password: str


class UserRegister(BaseModel):
    first_name: str
    password: str