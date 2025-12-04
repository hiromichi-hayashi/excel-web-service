from datetime import datetime

from pydantic import EmailStr
from sqlmodel import SQLModel


class UserBase(SQLModel):
    """ユーザーの基本スキーマ"""

    email: EmailStr
    username: str


class UserCreate(UserBase):
    """ユーザー作成スキーマ"""

    password: str


class UserUpdate(SQLModel):
    """ユーザー更新スキーマ"""

    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserRead(UserBase):
    """ユーザーレスポンススキーマ"""

    id: int
    created_at: datetime
    updated_at: datetime | None = None

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

    email: str | None = None
