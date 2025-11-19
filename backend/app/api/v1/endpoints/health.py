"""
ヘルスチェックエンドポイント
"""
from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "database": os.getenv("DATABASE_URL", "not configured")
    }
