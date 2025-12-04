from datetime import datetime

from sqlmodel import SQLModel


class TemplateRead(SQLModel):
    """テンプレート読み取りスキーマ"""

    id: int
    name: str
    description: str | None = None
    file_type: str
    thumbnail_path: str | None = None
    is_public: bool
    created_by: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class TemplateListResponse(SQLModel):
    """テンプレート一覧レスポンススキーマ"""

    items: list[TemplateRead]
    total: int
