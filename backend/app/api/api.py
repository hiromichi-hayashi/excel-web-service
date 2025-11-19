"""
APIルーター集約

すべてのエンドポイントをまとめる
"""
from fastapi import APIRouter

from app.api.endpoints import health, info

api_router = APIRouter()

# ヘルスチェック
api_router.include_router(health.router, tags=["health"])

# API情報
api_router.include_router(info.router, tags=["info"])
