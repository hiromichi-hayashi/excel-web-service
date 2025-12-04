from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """ユーザーマスターモデル"""

    __tablename__ = "m_user"

    # 基本情報
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False, max_length=255)
    username: str = Field(unique=True, index=True, nullable=False, max_length=50)
    password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: datetime | None = Field(
        default=None, sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)}
    )
