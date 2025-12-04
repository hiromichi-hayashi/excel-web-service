from datetime import datetime
from typing import Any

from pydantic import computed_field
from sqlmodel import SQLModel


class FileCreate(SQLModel):
    """ファイル作成スキーマ"""

    description: str | None = None


class FileUpdate(SQLModel):
    """ファイル更新スキーマ"""

    description: str | None = None


class FileRead(SQLModel):
    """ファイル読み取りスキーマ"""

    id: int
    user_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    rows_count: int | None = None
    columns_count: int | None = None
    sheets_count: int | None = None
    status: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    last_accessed_at: datetime | None = None

    class Config:
        from_attributes = True


class FileDataResponse(SQLModel):
    """ファイルデータレスポンススキーマ"""

    headers: list[str]
    rows: list[list[Any]]
    total_rows: int


class FileListResponse(SQLModel):
    """ファイル一覧レスポンススキーマ"""

    items: list[FileRead]
    total: int
    page: int
    page_size: int
    total_pages: int

    # 後方互換性: 'files' フィールドを 'items' のエイリアスとして提供
    # TODO: クライアントが 'items' に移行したら、このフィールドを削除する
    # Deprecated: 'files' フィールドは非推奨です。代わりに 'items' を使用してください。
    @computed_field
    @property
    def files(self) -> list[FileRead]:
        """Deprecated: Use 'items' instead. Kept for backwards compatibility."""
        return self.items


class StatisticsResponse(SQLModel):
    """統計情報レスポンススキーマ"""

    total_files: int
    total_templates: int
