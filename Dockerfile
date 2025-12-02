FROM python:3.14.0-slim

WORKDIR /app

# uvのインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# pyproject.tomlをコピー
COPY pyproject.toml .

# 依存関係をインストール
RUN uv pip install --system -r pyproject.toml

# アプリケーションコードをコピー
COPY . .

EXPOSE 8000
