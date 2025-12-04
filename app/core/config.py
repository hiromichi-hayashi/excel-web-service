import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """アプリケーション設定"""

    PROJECT_NAME: str = "Excel Web Service"
    VERSION: str = "1.0.0"

    # データベース
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/excel_web_service"
    )

    # JWT設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "2880"))  # 2日

    # ファイルストレージ設定
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: list[str] = [".xlsx", ".xls", ".csv"]
    MAX_ROWS_PREVIEW: int = 100  # プレビュー行数


settings = Settings()
