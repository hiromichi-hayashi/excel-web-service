from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from app.database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPIを使用したExcel処理Webサービス",
    version=settings.VERSION
)

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# API v1ルーターを追加
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Welcome to Excel Web Service",
        "docs": "/docs",
        "version": settings.VERSION,
    }


@app.get("/health")
async def health():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}
