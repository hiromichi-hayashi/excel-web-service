from typing import Optional, List
from sqlmodel import Session, select
from app.models.file import File
from datetime import datetime


def get_user_files(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[File]:
    """ユーザーのファイル一覧を取得"""
    statement = (
        select(File)
        .where(File.user_id == user_id)
        .order_by(File.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.exec(statement).all())


def count_user_files(db: Session, user_id: int) -> int:
    """ユーザーのファイル総数を取得"""
    statement = select(File).where(File.user_id == user_id)
    return len(list(db.exec(statement).all()))


def get_file(db: Session, file_id: int, user_id: int) -> Optional[File]:
    """ファイルを取得（ユーザー権限チェック付き）"""
    statement = select(File).where(File.id == file_id, File.user_id == user_id)
    return db.exec(statement).first()


def get_file_by_id(db: Session, file_id: int) -> Optional[File]:
    """ファイルをIDで取得（権限チェックなし）"""
    statement = select(File).where(File.id == file_id)
    return db.exec(statement).first()


def create_file(db: Session, file: File) -> File:
    """新規ファイルを作成"""
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def update_file(db: Session, file_id: int, **kwargs) -> Optional[File]:
    """ファイル情報を更新"""
    file = get_file_by_id(db, file_id)
    if not file:
        return None

    for key, value in kwargs.items():
        if hasattr(file, key) and value is not None:
            setattr(file, key, value)

    file.updated_at = datetime.utcnow()
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def delete_file(db: Session, file_id: int) -> bool:
    """ファイルを削除"""
    file = get_file_by_id(db, file_id)
    if not file:
        return False

    db.delete(file)
    db.commit()
    return True


def update_last_accessed(db: Session, file_id: int) -> None:
    """最終アクセス日時を更新"""
    file = get_file_by_id(db, file_id)
    if file:
        file.last_accessed_at = datetime.utcnow()
        db.add(file)
        db.commit()


def get_recent_files(db: Session, user_id: int, limit: int = 5) -> List[File]:
    """最近アクセスしたファイルを取得"""
    statement = (
        select(File)
        .where(File.user_id == user_id)
        .where(File.last_accessed_at.isnot(None))
        .order_by(File.last_accessed_at.desc())
        .limit(limit)
    )
    return list(db.exec(statement).all())
