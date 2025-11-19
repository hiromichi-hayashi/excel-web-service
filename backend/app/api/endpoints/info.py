"""
API情報エンドポイント
"""
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }


@router.get("/info")
async def api_info():
    """API情報"""
    return {
        "api_version": "v1",
        "python_version": "3.12",
        "framework": "FastAPI",
        "database": "PostgreSQL",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }
