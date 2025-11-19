from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI(
    title="Excel Web Service API",
    description="Excel処理を行うWebサービスのAPI",
    version="1.0.0"
)

# CORS設定（React開発環境用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Excel Web Service API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "database": os.getenv("DATABASE_URL", "not configured")
    }


@app.get("/api/v1/info")
async def api_info():
    """API情報エンドポイント"""
    return {
        "api_version": "v1",
        "python_version": "3.12",
        "framework": "FastAPI",
        "database": "PostgreSQL"
    }


# Static files設定（本番環境用）
# NOTE: このセクションは最後に配置すること（/{full_path:path}がすべてをキャッチするため）
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    # 静的アセット（JS, CSS, 画像など）をマウント
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="static")

    @app.get("/favicon.ico")
    async def favicon():
        """Favicon"""
        favicon_path = static_dir / "favicon.ico"
        if favicon_path.exists():
            return FileResponse(str(favicon_path))
        return {"detail": "Not found"}

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """SPAフォールバック（本番環境用）

        開発時: Vite dev server (localhost:3000) を使用
        本番時: ビルド済みの静的ファイルを配信
        """
        # 静的ファイルが存在する場合はそれを返す
        file_path = static_dir / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))

        # それ以外はindex.htmlを返す（SPAルーティング）
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))

        return {"detail": "Not found"}
