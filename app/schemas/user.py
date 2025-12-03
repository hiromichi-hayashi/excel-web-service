from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    """ユーザーの基本スキーマ"""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""
    password: str


class UserUpdate(SQLModel):
    """ユーザー更新スキーマ"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    """ユーザーレスポンススキーマ"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(SQLModel):
    """ユーザーログインスキーマ"""
    email: EmailStr
    password: str


class Token(SQLModel):
    """トークンレスポンススキーマ"""
    access_token: str
    token_type: str


class TokenData(SQLModel):
    """トークンペイロードスキーマ"""
    email: Optional[str] = None
