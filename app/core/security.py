from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8") if isinstance(hashed_password, str) else hashed_password,
    )


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化"""
    # bcrypt は72バイトまでしか対応していないため切り詰める
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWTアクセストークンを生成"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
