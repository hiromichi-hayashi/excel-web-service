from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Template(SQLModel, table=True):
    """テンプレートマスターモデル"""

    __tablename__ = "m_template"

    # 基本情報
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, nullable=False)
    description: str | None = Field(default=None, max_length=500)
    file_type: str = Field(max_length=10, nullable=False)
    file_path: str = Field(max_length=500, nullable=False)
    thumbnail_path: str | None = Field(default=None, max_length=500)

    # 公開設定
    is_public: bool = Field(default=True, nullable=False)
    created_by: int | None = Field(default=None, foreign_key="m_user.id")

    # タイムスタンプ
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
