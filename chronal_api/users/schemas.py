from typing import Literal

from pydantic import UUID4, EmailStr

from chronal_api.lib.schemas import BaseModel


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID4


# Access token


class CreateToken(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: UUID4
    token_type: Literal["bearer"]
