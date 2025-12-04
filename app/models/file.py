from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class File(SQLModel, table=True):
    """ファイルマスターモデル"""

    __tablename__ = "t_file"

    # 基本情報
    id: int | None = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="m_user.id", index=True)
    filename: str = Field(max_length=255, nullable=False)
    original_filename: str = Field(max_length=255, nullable=False)
    file_type: str = Field(max_length=10, nullable=False)  # xlsx, csv, xls
    file_size: int = Field(nullable=False)  # bytes
    file_path: str = Field(max_length=500, nullable=False)

    # メタデータ
    rows_count: int | None = Field(default=None)
    columns_count: int | None = Field(default=None)
    sheets_count: int | None = Field(default=None)

    # ステータス
    status: str = Field(default="uploaded", max_length=20)  # uploaded, processing, ready, error
    description: str | None = Field(default=None, max_length=500)

    # タイムスタンプ
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)}
    )
    last_accessed_at: datetime | None = Field(default=None)
