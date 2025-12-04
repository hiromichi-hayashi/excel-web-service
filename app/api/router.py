from fastapi import APIRouter

from app.api.endpoints import auth, files, templates

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["認証"])
api_router.include_router(files.router, prefix="/files", tags=["ファイル"])
api_router.include_router(templates.router, prefix="/templates", tags=["テンプレート"])
