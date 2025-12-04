from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional, List, Any
from pydantic import field_validator


class FileCreate(SQLModel):
    """ファイル作成スキーマ"""
    description: Optional[str] = None


class FileUpdate(SQLModel):
    """ファイル更新スキーマ"""
    description: Optional[str] = None


class FileRead(SQLModel):
    """ファイル読み取りスキーマ"""
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    rows_count: Optional[int] = None
    columns_count: Optional[int] = None
    sheets_count: Optional[int] = None
    status: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FileDataResponse(SQLModel):
    """ファイルデータレスポンススキーマ"""
    headers: List[str]
    rows: List[List[Any]]
    total_rows: int


class FileListResponse(SQLModel):
    """ファイル一覧レスポンススキーマ"""
    files: List[FileRead]
    total: int
    page: int
    page_size: int
