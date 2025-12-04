import os
from pathlib import Path
from typing import Optional, List, Tuple, Any
from sqlmodel import Session
from fastapi import UploadFile, HTTPException, status

from app.models.file import File
from app.repositories import file as file_repository
from app.core.storage import (
    save_upload_file,
    get_file_path,
    delete_file as delete_file_storage,
    validate_file_extension,
    get_file_size
)
from app.core.file_processor import FileProcessor
from app.core.config import settings


async def upload_file(
    db: Session,
    user_id: int,
    upload_file: UploadFile
) -> File:
    """
    ファイルをアップロード

    Args:
        db: データベースセッション
        user_id: ユーザーID
        upload_file: アップロードファイル

    Returns:
        作成されたFileモデル

    Raises:
        HTTPException: バリデーションエラーやファイルサイズ超過
    """
    # ファイル名とサイズの検証
    if not upload_file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ファイル名が無効です"
        )

    # 拡張子チェック
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"許可されていないファイル形式です。許可: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # ファイル内容を読み込み
    file_content = await upload_file.read()
    file_size = len(file_content)

    # サイズチェック
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"ファイルサイズが大きすぎます。最大: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )

    # ファイルを保存
    file_path = save_upload_file(user_id, file_content, upload_file.filename)
    file_type = os.path.splitext(upload_file.filename)[1].lower()

    # メタデータを抽出
    absolute_path = get_file_path(file_path)
    metadata = FileProcessor.extract_metadata(absolute_path, file_type)

    # データベースに保存
    db_file = File(
        user_id=user_id,
        filename=Path(file_path).name,
        original_filename=upload_file.filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        rows_count=metadata.get("rows_count"),
        columns_count=metadata.get("columns_count"),
        sheets_count=metadata.get("sheets_count"),
        status="ready"
    )

    return file_repository.create_file(db, db_file)


def get_file_data(
    db: Session,
    file_id: int,
    user_id: int,
    max_rows: Optional[int] = None
) -> Tuple[List[str], List[List[Any]], int]:
    """
    ファイルデータを取得

    Args:
        db: データベースセッション
        file_id: ファイルID
        user_id: ユーザーID
        max_rows: 最大行数

    Returns:
        (ヘッダー, 行データ, 総行数)

    Raises:
        HTTPException: ファイルが見つからない、権限なし
    """
    # ファイルを取得
    file = file_repository.get_file(db, file_id, user_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません"
        )

    # 最終アクセス日時を更新
    file_repository.update_last_accessed(db, file_id)

    # ファイルパスを取得
    file_path = get_file_path(file.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません（ストレージ）"
        )

    # プレビューデータを取得
    headers, rows = FileProcessor.get_preview_data(
        file_path,
        file.file_type,
        max_rows
    )

    total_rows = file.rows_count or len(rows)

    return headers, rows, total_rows


def get_user_files(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[File], int]:
    """
    ユーザーのファイル一覧を取得

    Args:
        db: データベースセッション
        user_id: ユーザーID
        skip: スキップ件数
        limit: 取得件数

    Returns:
        (ファイルリスト, 総数)
    """
    files = file_repository.get_user_files(db, user_id, skip, limit)
    total = file_repository.count_user_files(db, user_id)
    return files, total


def get_file(db: Session, file_id: int, user_id: int) -> File:
    """
    ファイルを取得

    Args:
        db: データベースセッション
        file_id: ファイルID
        user_id: ユーザーID

    Returns:
        Fileモデル

    Raises:
        HTTPException: ファイルが見つからない
    """
    file = file_repository.get_file(db, file_id, user_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません"
        )
    return file


def delete_file(db: Session, file_id: int, user_id: int) -> bool:
    """
    ファイルを削除

    Args:
        db: データベースセッション
        file_id: ファイルID
        user_id: ユーザーID

    Returns:
        削除成功したか

    Raises:
        HTTPException: ファイルが見つからない、権限なし
    """
    # ファイルを取得
    file = file_repository.get_file(db, file_id, user_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません"
        )

    # ストレージからファイルを削除
    delete_file_storage(file.file_path)

    # データベースから削除
    return file_repository.delete_file(db, file_id)


def update_file(
    db: Session,
    file_id: int,
    user_id: int,
    description: Optional[str] = None
) -> File:
    """
    ファイル情報を更新

    Args:
        db: データベースセッション
        file_id: ファイルID
        user_id: ユーザーID
        description: 説明

    Returns:
        更新されたFileモデル

    Raises:
        HTTPException: ファイルが見つからない、権限なし
    """
    # ファイルを取得して権限チェック
    file = file_repository.get_file(db, file_id, user_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ファイルが見つかりません"
        )

    # 更新
    updated_file = file_repository.update_file(
        db,
        file_id,
        description=description
    )

    if not updated_file:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ファイルの更新に失敗しました"
        )

    return updated_file


def get_recent_files(db: Session, user_id: int, limit: int = 5) -> List[File]:
    """
    最近アクセスしたファイルを取得

    Args:
        db: データベースセッション
        user_id: ユーザーID
        limit: 取得件数

    Returns:
        ファイルリスト
    """
    return file_repository.get_recent_files(db, user_id, limit)
