from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class Template(SQLModel, table=True):
    """テンプレートマスターモデル"""
    __tablename__ = "m_template"

    # 基本情報
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None, max_length=500)
    file_type: str = Field(max_length=10, nullable=False)
    file_path: str = Field(max_length=500, nullable=False)
    thumbnail_path: Optional[str] = Field(default=None, max_length=500)

    # 公開設定
    is_public: bool = Field(default=True, nullable=False)
    created_by: Optional[int] = Field(default=None, foreign_key="m_user.id")

    # タイムスタンプ
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
