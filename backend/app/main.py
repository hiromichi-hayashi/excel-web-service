"""
FastAPI メインアプリケーション

エントリーポイント
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.core.config import settings
from app.api.v1.api import api_router


def create_application() -> FastAPI:
    """
    FastAPIアプリケーションファクトリ

    設定に基づいてアプリケーションを構築
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # APIルーターの登録
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Static files設定（本番環境用）
    # NOTE: このセクションは最後に配置すること（/{full_path:path}がすべてをキャッチするため）
    setup_static_files(app)

    return app


def setup_static_files(app: FastAPI) -> None:
    """
    静的ファイル配信の設定

    本番環境: ビルド済みフロントエンドを配信
    開発環境: Vite dev serverを使用（このコードは実行されない）
    """
    static_dir = Path(__file__).parent / "static"

    if not static_dir.exists():
        return

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
        """
        SPAフォールバック（本番環境用）

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


# アプリケーションインスタンスの作成
app = create_application()
