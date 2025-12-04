"""Rename users to m_user and add new columns

Revision ID: d74f2f5a7a56
Revises: b6583118307c
Create Date: 2025-12-03 13:51:42.702753

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d74f2f5a7a56"
down_revision: str | Sequence[str] | None = "b6583118307c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # テーブル名を変更（データを保持）
    op.rename_table("users", "m_user")

    # インデックス名を変更
    op.execute("ALTER INDEX ix_users_id RENAME TO ix_m_user_id")
    op.execute("ALTER INDEX ix_users_email RENAME TO ix_m_user_email")
    op.execute("ALTER INDEX ix_users_username RENAME TO ix_m_user_username")
    op.execute("ALTER SEQUENCE users_id_seq RENAME TO m_user_id_seq")

    # 新しいカラムを追加
    op.add_column("m_user", sa.Column("full_name", sa.String(length=100), nullable=True))
    op.add_column("m_user", sa.Column("phone_number", sa.String(length=20), nullable=True))
    op.add_column("m_user", sa.Column("profile_image_url", sa.String(length=500), nullable=True))
    op.add_column("m_user", sa.Column("bio", sa.String(length=1000), nullable=True))
    op.add_column(
        "m_user",
        sa.Column("is_email_verified", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column("m_user", sa.Column("last_login_at", sa.DateTime(), nullable=True))

    # 既存カラムの制約を更新
    op.alter_column("m_user", "is_active", nullable=False, server_default="true")
    op.alter_column("m_user", "is_superuser", nullable=False, server_default="false")
    op.alter_column("m_user", "created_at", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 新しいカラムを削除
    op.drop_column("m_user", "last_login_at")
    op.drop_column("m_user", "is_email_verified")
    op.drop_column("m_user", "bio")
    op.drop_column("m_user", "profile_image_url")
    op.drop_column("m_user", "phone_number")
    op.drop_column("m_user", "full_name")

    # 制約を元に戻す
    op.alter_column("m_user", "is_active", nullable=True)
    op.alter_column("m_user", "is_superuser", nullable=True)
    op.alter_column("m_user", "created_at", nullable=True)

    # テーブル名を元に戻す
    op.rename_table("m_user", "users")

    # インデックス名を元に戻す
    op.execute("ALTER INDEX ix_m_user_id RENAME TO ix_users_id")
    op.execute("ALTER INDEX ix_m_user_email RENAME TO ix_users_email")
    op.execute("ALTER INDEX ix_m_user_username RENAME TO ix_users_username")
    op.execute("ALTER SEQUENCE m_user_id_seq RENAME TO users_id_seq")
