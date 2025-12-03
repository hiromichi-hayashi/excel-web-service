from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories import user as user_repository
from app.core.security import get_password_hash, verify_password


def register_user(db: Session, user: UserCreate) -> User:
    """新規ユーザー登録（重複チェック込み）"""
    # メールアドレスの重複チェック
    if user_repository.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に登録されています"
        )

    # ユーザー名の重複チェック
    if user_repository.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このユーザー名は既に使用されています"
        )

    # パスワードをハッシュ化してユーザー作成
    hashed_password = get_password_hash(user.password)
    return user_repository.create_user(
        db=db,
        email=user.email,
        username=user.username,
        password=hashed_password
    )


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """ユーザー認証（emailベース）"""
    user = user_repository.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """ユーザー情報を更新"""
    update_data = user_update.model_dump(exclude_unset=True)

    # パスワードが含まれている場合はハッシュ化
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    return user_repository.update_user(db, user_id, **update_data)


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """IDでユーザーを取得"""
    return user_repository.get_user(db, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """メールアドレスでユーザーを取得"""
    return user_repository.get_user_by_email(db, email)
