from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPIを使用したExcel処理Webサービス",
    version=settings.VERSION
)

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# APIルーターを追加
app.include_router(api_router, prefix="/api")


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
