from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Query, status
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.database.database import get_db
from app.api.endpoints.auth import get_current_active_user
from app.models.user import User
from app.schemas.file import (
    FileRead,
    FileUpdate,
    FileDataResponse,
    FileListResponse
)
from app.services import file as file_service
from app.core.storage import get_file_path

router = APIRouter()


@router.post("/upload", response_model=FileRead, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルをアップロード"""
    uploaded_file = await file_service.upload_file(db, current_user.id, file)
    return uploaded_file


@router.get("", response_model=FileListResponse)
def list_files(
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(20, ge=1, le=100, description="ページサイズ"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイル一覧を取得"""
    skip = (page - 1) * page_size
    files, total = file_service.get_user_files(db, current_user.id, skip, page_size)

    return FileListResponse(
        files=files,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/recent", response_model=list[FileRead])
def get_recent_files(
    limit: int = Query(5, ge=1, le=20, description="取得件数"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """最近アクセスしたファイルを取得"""
    files = file_service.get_recent_files(db, current_user.id, limit)
    return files


@router.get("/{file_id}", response_model=FileRead)
def get_file(
    file_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルメタデータを取得"""
    file = file_service.get_file(db, file_id, current_user.id)
    return file


@router.get("/{file_id}/data", response_model=FileDataResponse)
def get_file_data(
    file_id: int,
    max_rows: int = Query(None, ge=1, le=1000, description="最大行数"),
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルデータを取得（グリッド表示用）"""
    headers, rows, total_rows = file_service.get_file_data(
        db, file_id, current_user.id, max_rows
    )

    return FileDataResponse(
        headers=headers,
        rows=rows,
        total_rows=total_rows
    )


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルをダウンロード"""
    file = file_service.get_file(db, file_id, current_user.id)
    file_path = get_file_path(file.file_path)

    return FileResponse(
        path=str(file_path),
        filename=file.original_filename,
        media_type="application/octet-stream"
    )


@router.patch("/{file_id}", response_model=FileRead)
def update_file(
    file_id: int,
    file_update: FileUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルメタデータを更新"""
    updated_file = file_service.update_file(
        db,
        file_id,
        current_user.id,
        description=file_update.description
    )
    return updated_file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Session = Depends(get_db)
):
    """ファイルを削除"""
    file_service.delete_file(db, file_id, current_user.id)
    return None
