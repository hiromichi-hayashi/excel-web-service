import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.router import api_router
from app.core.config import settings
from app.database import engine, Base
from app.models import User  # モデルをインポートしてBase.metadataに登録

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPIを使用したExcel処理Webサービス",
    version=settings.VERSION
)

# CORS設定（開発環境用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite開発サーバー
        "http://localhost:8000",  # FastAPI
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# APIルーターを追加
app.include_router(api_router, prefix="/api")

# 静的ファイル配信（本番環境用）
# frontend/dist/ が存在する場合のみマウント
frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """フロントエンドのSPAルーティング対応"""
        # API以外のルートはReactアプリを返す
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("health"):
            return {"detail": "Not Found"}

        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # SPAなので全てindex.htmlを返す
        return FileResponse(frontend_dist / "index.html")


@app.get("/health")
async def health():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}
