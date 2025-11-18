from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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
