import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """アプリケーション設定"""
    PROJECT_NAME: str = "Excel Web Service"
    VERSION: str = "1.0.0"

    # データベース
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/excel_web_service")

    # JWT設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()
