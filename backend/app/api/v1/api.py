"""
APIルーター集約

すべてのv1エンドポイントをまとめる
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, info

api_router = APIRouter()

# ヘルスチェック（プレフィックスなし）
api_router.include_router(health.router, tags=["health"])

# API情報（/api/v1プレフィックス）
api_router.include_router(info.router, tags=["info"])
