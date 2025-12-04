import os
from collections.abc import Generator

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/excel_web_service")

engine = create_engine(DATABASE_URL, echo=False)


def get_db() -> Generator[Session]:
    """データベースセッションの依存関係"""
    with Session(engine) as session:
        yield session
