from fastapi import FastAPI
import os

app = FastAPI(
    title="Excel Web Service",
    description="FastAPIを使用したExcel処理Webサービス",
    version="1.0.0"
)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Welcome to Excel Web Service",
        "docs": "/docs",
        "python_version": "3.14.0",
        "database": os.getenv("DATABASE_URL", "Not configured")
    }


@app.get("/api/info")
async def info():
    """システム情報エンドポイント"""
    return {
        "app_name": "Excel Web Service",
        "version": "1.0.0",
        "environment": {
            "database_url": os.getenv("DATABASE_URL", "Not set"),
            "pythonunbuffered": os.getenv("PYTHONUNBUFFERED", "Not set")
        }
    }
