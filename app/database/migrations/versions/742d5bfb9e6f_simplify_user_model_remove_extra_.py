"""Simplify user model - remove extra columns and rename password field

Revision ID: 742d5bfb9e6f
Revises: d74f2f5a7a56
Create Date: 2025-12-03 14:07:39.438225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '742d5bfb9e6f'
down_revision: Union[str, Sequence[str], None] = 'd74f2f5a7a56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # hashed_password を password にリネーム（データを保持）
    op.alter_column('m_user', 'hashed_password', new_column_name='password')

    # 不要なカラムを削除
    op.drop_column('m_user', 'full_name')
    op.drop_column('m_user', 'bio')
    op.drop_column('m_user', 'is_email_verified')
    op.drop_column('m_user', 'phone_number')
    op.drop_column('m_user', 'is_active')
    op.drop_column('m_user', 'is_superuser')
    op.drop_column('m_user', 'last_login_at')
    op.drop_column('m_user', 'profile_image_url')


def downgrade() -> None:
    """Downgrade schema."""
    # 削除したカラムを再追加
    op.add_column('m_user', sa.Column('profile_image_url', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.add_column('m_user', sa.Column('last_login_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('m_user', sa.Column('is_superuser', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('m_user', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.add_column('m_user', sa.Column('phone_number', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('m_user', sa.Column('is_email_verified', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.add_column('m_user', sa.Column('bio', sa.VARCHAR(length=1000), autoincrement=False, nullable=True))
    op.add_column('m_user', sa.Column('full_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))

    # password を hashed_password にリネーム
    op.alter_column('m_user', 'password', new_column_name='hashed_password')
