from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class File(SQLModel, table=True):
    """ファイルマスターモデル"""
    __tablename__ = "t_file"

    # 基本情報
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="m_user.id", index=True)
    filename: str = Field(max_length=255, nullable=False)
    original_filename: str = Field(max_length=255, nullable=False)
    file_type: str = Field(max_length=10, nullable=False)  # xlsx, csv, xls
    file_size: int = Field(nullable=False)  # bytes
    file_path: str = Field(max_length=500, nullable=False)

    # メタデータ
    rows_count: Optional[int] = Field(default=None)
    columns_count: Optional[int] = Field(default=None)
    sheets_count: Optional[int] = Field(default=None)

    # ステータス
    status: str = Field(default="uploaded", max_length=20)  # uploaded, processing, ready, error
    description: Optional[str] = Field(default=None, max_length=500)

    # タイムスタンプ
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})
    last_accessed_at: Optional[datetime] = Field(default=None)
