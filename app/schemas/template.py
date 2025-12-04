from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional, List


class TemplateRead(SQLModel):
    """テンプレート読み取りスキーマ"""
    id: int
    name: str
    description: Optional[str] = None
    file_type: str
    thumbnail_path: Optional[str] = None
    is_public: bool
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TemplateListResponse(SQLModel):
    """テンプレート一覧レスポンススキーマ"""
    templates: List[TemplateRead]
    total: int
