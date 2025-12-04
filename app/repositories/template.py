from typing import Optional, List
from sqlmodel import Session, select
from app.models.template import Template


def get_templates(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_public: Optional[bool] = None
) -> List[Template]:
    """テンプレート一覧を取得"""
    statement = select(Template).offset(skip).limit(limit)

    if is_public is not None:
        statement = statement.where(Template.is_public == is_public)

    statement = statement.order_by(Template.created_at.desc())
    return list(db.exec(statement).all())


def count_templates(db: Session, is_public: Optional[bool] = None) -> int:
    """テンプレート総数を取得"""
    statement = select(Template)

    if is_public is not None:
        statement = statement.where(Template.is_public == is_public)

    return len(list(db.exec(statement).all()))


def get_template(db: Session, template_id: int) -> Optional[Template]:
    """テンプレートをIDで取得"""
    statement = select(Template).where(Template.id == template_id)
    return db.exec(statement).first()


def create_template(db: Session, template: Template) -> Template:
    """新規テンプレートを作成"""
    db.add(template)
    db.commit()
    db.refresh(template)
    return template
