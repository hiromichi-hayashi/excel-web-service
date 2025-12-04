from sqlmodel import Session, select

from app.models.user import User


def get_user(db: Session, user_id: int) -> User | None:
    """IDでユーザーを取得"""
    statement = select(User).where(User.id == user_id)
    return db.exec(statement).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """メールアドレスでユーザーを取得"""
    statement = select(User).where(User.email == email)
    return db.exec(statement).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """ユーザー名でユーザーを取得"""
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """ユーザー一覧を取得"""
    statement = select(User).offset(skip).limit(limit)
    return list(db.exec(statement).all())


def create_user(db: Session, email: str, username: str, password: str) -> User:
    """新規ユーザーを作成"""
    db_user = User(
        email=email,
        username=username,
        password=password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, **kwargs) -> User | None:
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
