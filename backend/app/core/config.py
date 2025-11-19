"""
アプリケーション設定

Pydantic Settingsを使用した型安全な設定管理
環境変数から設定を読み込み
"""
from typing import Any, Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # API設定
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Excel Web Service API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Excel処理を行うWebサービスのAPI"

    # CORS設定
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # データベース設定
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "excel_web_service"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        """データベースURL を構築"""
        if isinstance(v, str):
            return v

        # 環境変数から構築
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=info.data.get("POSTGRES_PORT"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        )

    # セキュリティ設定
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 開発環境設定
    DEBUG: bool = True


# グローバル設定インスタンス
settings = Settings()
