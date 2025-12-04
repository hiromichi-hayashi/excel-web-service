from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.file import File


def get_user_files(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[File]:
    """ユーザーのファイル一覧を取得（削除中のファイルは除外）"""
    statement = (
        select(File)
        .where(File.user_id == user_id)
        .where(File.status != "deleting")  # 削除中のファイルを除外
        .order_by(File.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.exec(statement).all())


def count_user_files(db: Session, user_id: int) -> int:
    """ユーザーのファイル総数を取得（削除中のファイルは除外）"""
    statement = (
        select(func.count(File.id))
        .where(File.user_id == user_id)
        .where(File.status != "deleting")  # 削除中のファイルを除外
    )
    return db.exec(statement).one()


def get_file(db: Session, file_id: int, user_id: int) -> File | None:
    """ファイルを取得（ユーザー権限チェック付き）"""
    statement = select(File).where(File.id == file_id, File.user_id == user_id)
    return db.exec(statement).first()


def get_file_by_id(db: Session, file_id: int) -> File | None:
    """ファイルをIDで取得（権限チェックなし）"""
    statement = select(File).where(File.id == file_id)
    return db.exec(statement).first()


def create_file(db: Session, file: File) -> File:
    """新規ファイルを作成"""
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def update_file(db: Session, file_id: int, user_id: int, **kwargs) -> File | None:
    """ファイル情報を更新（ユーザー権限チェック付き）"""
    file = get_file(db, file_id, user_id)
    if not file:
        return None

    for key, value in kwargs.items():
        if hasattr(file, key):
            setattr(file, key, value)

    file.updated_at = datetime.now(UTC)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def delete_file(db: Session, file_id: int, user_id: int) -> bool:
    """ファイルを削除（ユーザー権限チェック付き）"""
    file = get_file(db, file_id, user_id)
    if not file:
        return False

    db.delete(file)
    db.commit()
    return True


def update_last_accessed(db: Session, file_id: int, user_id: int) -> None:
    """最終アクセス日時を更新（ユーザー権限チェック付き、削除中は除外）"""
    file = get_file(db, file_id, user_id)
    if file and file.status != "deleting":
        file.last_accessed_at = datetime.now(UTC)
        db.add(file)
        db.commit()


def get_recent_files(db: Session, user_id: int, limit: int = 5) -> list[File]:
    """最近アクセスしたファイルを取得（削除中のファイルは除外）"""
    statement = (
        select(File)
        .where(File.user_id == user_id)
        .where(File.last_accessed_at.isnot(None))
        .where(File.status != "deleting")  # 削除中のファイルを除外
        .order_by(File.last_accessed_at.desc())
        .limit(limit)
    )
    return list(db.exec(statement).all())


def get_user_statistics(db: Session, user_id: int) -> dict[str, Any]:
    """
    ユーザーの統計情報を取得（削除中のファイルは除外）

    Args:
        db: データベースセッション
        user_id: ユーザーID

    Returns:
        統計情報の辞書 (total_files, total_templates)
    """
    from app.repositories import template as template_repository

    # ファイル数を取得（count_user_files が既に削除中のファイルを除外）
    total_files = count_user_files(db, user_id)

    # 公開テンプレート数を取得
    total_templates = template_repository.count_templates(db, is_public=True)

    return {
        "total_files": total_files,
        "total_templates": total_templates,
    }


def get_files_by_status(db: Session, status: str, limit: int = 100) -> list[File]:
    """
    指定されたステータスのファイルを取得（orphaned recordのクリーンアップ用）

    Args:
        db: データベースセッション
        status: ファイルステータス（例: "deleting"）
        limit: 取得件数上限

    Returns:
        ファイルリスト
    """
    statement = (
        select(File).where(File.status == status).order_by(File.updated_at.desc()).limit(limit)
    )
    return list(db.exec(statement).all())


def hard_delete_file_by_id(db: Session, file_id: int) -> bool:
    """
    ファイルをIDで完全削除（権限チェックなし、クリーンアップ用）

    Args:
        db: データベースセッション
        file_id: ファイルID

    Returns:
        削除成功したか

    Note:
        この関数は管理者用のクリーンアップ処理で使用します。
        通常の削除処理では delete_file を使用してください。
    """
    file = get_file_by_id(db, file_id)
    if not file:
        return False

    db.delete(file)
    db.commit()
    return True
