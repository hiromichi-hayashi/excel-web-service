from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# SQLModel のモジュールをインポート
from sqlmodel import SQLModel
from app.models.user import User  # モデルをインポートしてメタデータに登録
from app.models.file import File
from app.models.template import Template

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 環境変数からデータベースURLを取得
# WARNING: 本番環境では必ずDATABASE_URL環境変数を設定してください
# デフォルト値は開発環境専用で、本番環境では絶対に使用しないでください
database_url = os.getenv("DATABASE_URL")

if database_url is None:
    # 開発環境用のローカルプレースホルダー（本番環境では使用不可）
    database_url = "postgresql://localhost:5432/excel_web_service_dev"
    print("WARNING: DATABASE_URL is not set. Using local development placeholder.")
    print("WARNING: This configuration must NOT be used in production!")

config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
