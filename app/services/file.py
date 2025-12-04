import asyncio
import logging
import os
from functools import partial
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlmodel import Session

from app.core.config import settings
from app.core.file_processor import FileProcessor
from app.core.storage import delete_file as delete_file_storage
from app.core.storage import get_file_path, save_upload_file, validate_file_extension
from app.models.file import File
from app.repositories import file as file_repository

logger = logging.getLogger(__name__)


async def upload_file(db: Session, user_id: int, upload_file: UploadFile) -> File:
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ファイル名が無効です")

    # 拡張子チェック
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"許可されていないファイル形式です。許可: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    # ファイル内容を読み込み
    file_content = await upload_file.read()
    file_size = len(file_content)

    # サイズチェック
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"ファイルサイズが大きすぎます。最大: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB",
        )

    # ファイルを保存（非同期実行）
    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(
        None, partial(save_upload_file, user_id, file_content, upload_file.filename)
    )
    file_type = os.path.splitext(upload_file.filename)[1].lower()

    # メタデータを抽出（非同期実行）
    absolute_path = get_file_path(file_path)
    metadata = await loop.run_in_executor(
        None, partial(FileProcessor.extract_metadata, absolute_path, file_type)
    )

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
        status="ready",
    )

    # データベースに保存（セッションはスレッドセーフではないため同期的に実行）
    return file_repository.create_file(db, db_file)


def get_file_data(
    db: Session, file_id: int, user_id: int, max_rows: int | None = None
) -> tuple[list[str], list[list[Any]], int]:
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
            status_code=status.HTTP_404_NOT_FOUND, detail="ファイルが見つかりません"
        )

    # 最終アクセス日時を更新
    file_repository.update_last_accessed(db, file_id)

    # ファイルパスを取得
    file_path = get_file_path(file.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ファイルが見つかりません（ストレージ）"
        )

    # プレビューデータを取得
    headers, rows = FileProcessor.get_preview_data(file_path, file.file_type, max_rows)

    total_rows = file.rows_count if file.rows_count is not None else len(rows)

    return headers, rows, total_rows


def get_user_files(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> tuple[list[File], int]:
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
            status_code=status.HTTP_404_NOT_FOUND, detail="ファイルが見つかりません"
        )
    return file


def delete_file(db: Session, file_id: int, user_id: int) -> bool:
    """
    ファイルを削除（3段階の安全な削除パターン）

    Args:
        db: データベースセッション
        file_id: ファイルID
        user_id: ユーザーID

    Returns:
        削除成功したか

    Raises:
        HTTPException: ファイルが見つからない、権限なし、削除失敗
    """
    # ファイルを取得
    file = file_repository.get_file(db, file_id, user_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ファイルが見つかりません"
        )

    # ファイルパスと元のステータスを保存
    file_path = file.file_path
    original_status = file.status

    # ステップ1: ソフトデリート（DB上でステータスを"deleting"にマーク）
    # これにより、削除処理中のファイルが他の操作から隔離される
    try:
        updated_file = file_repository.update_file(db, file_id, user_id, status="deleting")
        if not updated_file:
            logger.error(f"ステータス更新に失敗しました。file_id={file_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="削除処理の開始に失敗しました",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ステータス更新中に例外が発生しました。file_id={file_id}, error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="削除処理の開始に失敗しました"
        ) from e

    # ステップ2: ストレージからファイルを削除
    try:
        storage_deleted = delete_file_storage(file_path)
        if not storage_deleted:
            # ストレージ削除失敗 → ステータスを元に戻す（ロールバック）
            logger.warning(
                f"ストレージ削除に失敗しました。ステータスをロールバックします。"
                f"file_id={file_id}, path={file_path}"
            )
            file_repository.update_file(db, file_id, user_id, status=original_status)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ストレージからのファイル削除に失敗しました",
            )
    except HTTPException:
        raise
    except Exception as e:
        # 例外発生 → ステータスを元に戻す（ロールバック）
        logger.error(
            f"ストレージ削除中に例外が発生しました。ステータスをロールバックします。"
            f"file_id={file_id}, path={file_path}, error={str(e)}"
        )
        try:
            file_repository.update_file(db, file_id, user_id, status=original_status)
        except Exception as rollback_error:
            logger.error(
                f"ロールバックに失敗しました。手動での確認が必要です。"
                f"file_id={file_id}, error={str(rollback_error)}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ストレージ削除中にエラーが発生しました",
        ) from e

    # ステップ3: データベースから完全削除（ハードデリート）
    db_deleted = file_repository.delete_file(db, file_id, user_id)
    if not db_deleted:
        # DB削除失敗 → ストレージは既に削除済み
        # orphaned recordとして残るが、status="deleting"なので後でクリーンアップ可能
        logger.error(
            f"データベース削除に失敗しました。orphaned recordが発生しました。"
            f"file_id={file_id}, path={file_path}, status=deleting"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="データベースからの削除に失敗しました",
        )

    logger.info(f"ファイル削除が正常に完了しました。file_id={file_id}, path={file_path}")
    return True


def update_file(db: Session, file_id: int, user_id: int, description: str | None = None) -> File:
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
            status_code=status.HTTP_404_NOT_FOUND, detail="ファイルが見つかりません"
        )

    # 更新
    updated_file = file_repository.update_file(db, file_id, user_id, description=description)

    if not updated_file:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="ファイルの更新に失敗しました"
        )

    return updated_file


def get_recent_files(db: Session, user_id: int, limit: int = 5) -> list[File]:
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


def get_user_statistics(db: Session, user_id: int) -> dict:
    """
    ユーザーの統計情報を取得

    Args:
        db: データベースセッション
        user_id: ユーザーID

    Returns:
        統計情報の辞書 (total_files, total_size, total_rows)
    """
    return file_repository.get_user_statistics(db, user_id)


def cleanup_orphaned_records(db: Session, limit: int = 100) -> dict:
    """
    orphaned recordsをクリーンアップ（管理者用）

    status="deleting" のレコードを検索し、物理ファイルが存在しない場合は
    DBレコードを削除する。削除処理が中断された場合の復旧に使用。

    Args:
        db: データベースセッション
        limit: 処理件数上限

    Returns:
        クリーンアップ結果 {checked: 件数, deleted: 件数, errors: エラー数}
    """
    # status="deleting" のファイルを取得
    deleting_files = file_repository.get_files_by_status(db, "deleting", limit)

    checked = 0
    deleted = 0
    errors = 0

    for file in deleting_files:
        checked += 1
        try:
            # 物理ファイルの存在確認（パストラバーサル対策付き）
            try:
                file_path = get_file_path(file.file_path)
                file_exists = file_path.exists()
            except ValueError:
                # パスが不正な場合は物理ファイルなしとして扱う
                file_exists = False

            if not file_exists:
                # 物理ファイルが存在しない場合、orphaned recordとして削除
                if file_repository.hard_delete_file_by_id(db, file.id):
                    deleted += 1
                    logger.info(
                        f"Orphaned recordを削除しました。file_id={file.id}, path={file.file_path}"
                    )
                else:
                    errors += 1
                    logger.error(f"Orphaned recordの削除に失敗しました。file_id={file.id}")
            else:
                # 物理ファイルが存在する場合はログ出力のみ（手動確認が必要）
                logger.warning(
                    f"status='deleting' だが物理ファイルが存在します。手動確認が必要です。"
                    f"file_id={file.id}, path={file.file_path}"
                )
        except Exception as e:
            errors += 1
            logger.error(
                f"クリーンアップ処理中にエラーが発生しました。file_id={file.id}, error={str(e)}"
            )

    result = {"checked": checked, "deleted": deleted, "errors": errors}

    logger.info(f"Orphaned recordsクリーンアップ完了: {result}")
    return result
