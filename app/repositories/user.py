from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User


def get_user(db: Session, user_id: int) -> Optional[User]:
    """IDでユーザーを取得"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """メールアドレスでユーザーを取得"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """ユーザー名でユーザーを取得"""
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """ユーザー一覧を取得"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, username: str, hashed_password: str) -> User:
    """新規ユーザーを作成"""
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    """ユーザー情報を更新"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    for field, value in kwargs.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """ユーザーを削除"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
