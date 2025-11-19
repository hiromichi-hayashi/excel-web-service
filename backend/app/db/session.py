"""
データベースセッション管理

SQLAlchemyセッションの作成と管理
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# SQLAlchemyエンジンの作成
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,  # 接続チェック
    echo=settings.DEBUG,  # SQLログ出力（開発時のみ）
)

# セッションファクトリの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    データベースセッションの依存性注入

    FastAPIのDependsで使用
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
