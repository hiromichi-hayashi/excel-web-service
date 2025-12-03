from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """ユーザーの基本スキーマ"""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""
    password: str


class UserUpdate(BaseModel):
    """ユーザー更新スキーマ"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """データベース内のユーザースキーマ"""
    id: int
    hashed_password: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class User(UserBase):
    """ユーザーレスポンススキーマ"""
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """トークンレスポンススキーマ"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """トークンペイロードスキーマ"""
    username: Optional[str] = None
