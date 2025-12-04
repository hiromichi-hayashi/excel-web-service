from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.api.endpoints.auth import get_current_active_user
from app.database.database import get_db
from app.models.user import User
from app.repositories import template as template_repository
from app.schemas.template import TemplateListResponse, TemplateRead

router = APIRouter()


@router.get("", response_model=TemplateListResponse)
def list_templates(
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1, description="ページ番号"),
    page_size: int = Query(20, ge=1, le=100, description="ページサイズ"),
):
    """テンプレート一覧を取得（公開テンプレートのみ）"""
    skip = (page - 1) * page_size
    templates = template_repository.get_templates(db, skip, page_size, is_public=True)
    total = template_repository.count_templates(db, is_public=True)

    return TemplateListResponse(items=templates, total=total)


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(template_id: int, db: Annotated[Session, Depends(get_db)]):
    """テンプレートを取得（公開テンプレートのみ）"""
    template = template_repository.get_template(db, template_id, is_public=True)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="テンプレートが見つかりません"
        )

    return template


@router.post("/{template_id}/use", status_code=status.HTTP_201_CREATED)
def use_template(
    template_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """テンプレートから新規ファイルを作成"""
    # TODO: Phase 2で実装
    # テンプレートファイルをコピーしてユーザーのファイルとして作成
    # IMPORTANT: template_repository.get_template(db, template_id, is_public=True) を使用して
    # 公開テンプレートのみアクセス可能にすること
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="この機能は今後実装予定です"
    )
