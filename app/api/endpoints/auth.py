from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, TokenData, UserCreate, UserLogin, UserRead
from app.services import user as user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    """現在のユーザーを取得"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception from None

    user = user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """アクティブなユーザーを取得"""
    return current_user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """新規ユーザー登録"""
    return user_service.register_user(db=db, user=user)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """ログイン（emailとパスワード）"""
    user = user_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """現在のユーザー情報を取得"""
    return current_user
