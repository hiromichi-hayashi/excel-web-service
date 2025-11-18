# Excel Web Service

Excel処理を行うWebサービス

## 技術スタック

### バックエンド
- **Python**: 3.12
- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL 16
- **実行環境**: Docker

### フロントエンド
- **Node.js**: 22.18.0 (ローカル環境)
- **フレームワーク**: React

## 環境構築

### 前提条件

- Docker & Docker Compose がインストールされていること
- Node.js 22.18.0 がインストールされていること（フロントエンド用）
- Git がインストールされていること

### セットアップ手順

#### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd excel-web-service
```

#### 2. 環境変数の設定

```bash
cp .env.example .env
```

必要に応じて `.env` ファイルを編集してください。

#### 3. バックエンド（FastAPI + PostgreSQL）の起動

Docker Composeを使用してバックエンドとデータベースを起動します：

```bash
docker-compose up -d
```

起動確認：

```bash
# コンテナの状態確認
docker-compose ps

# ログの確認
docker-compose logs -f backend

# ヘルスチェック
curl http://localhost:8000/health
```

#### 4. フロントエンド（React）の起動

フロントエンドはローカルのNode.js環境で実行します：

```bash
cd frontend
npm install
npm run dev
```

フロントエンドは `http://localhost:3000` で起動します。

## 開発用コマンド

### バックエンド

```bash
# コンテナの起動
docker-compose up -d

# コンテナの停止
docker-compose down

# コンテナの再起動
docker-compose restart

# ログの確認
docker-compose logs -f backend

# バックエンドコンテナに入る
docker-compose exec backend bash

# データベースに接続
docker-compose exec db psql -U postgres -d excel_web_service

# テストの実行
docker-compose exec backend pytest

# コードフォーマット
docker-compose exec backend black app/

# リンターの実行
docker-compose exec backend flake8 app/
```

### データベース

```bash
# データベースのリセット
docker-compose down -v
docker-compose up -d

# マイグレーション（Alembic）
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic revision --autogenerate -m "migration message"
```

## APIドキュメント

FastAPIの自動生成ドキュメントは以下のURLで確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## プロジェクト構造

```
excel-web-service/
├── backend/                # FastAPIバックエンド
│   ├── app/               # アプリケーションコード
│   │   ├── __init__.py
│   │   └── main.py        # メインアプリケーション
│   ├── Dockerfile         # Dockerイメージ定義
│   └── requirements.txt   # Python依存パッケージ
├── frontend/              # Reactフロントエンド
├── docker-compose.yml     # Docker Compose設定
├── .env.example          # 環境変数のサンプル
├── .gitignore            # Git除外設定
└── README.md             # このファイル
```

## トラブルシューティング

### ポートが既に使用されている

```bash
# 使用中のポートを確認
sudo lsof -i :8000
sudo lsof -i :5432

# プロセスを終了するか、docker-compose.ymlのポート設定を変更
```

### データベース接続エラー

```bash
# データベースコンテナが起動しているか確認
docker-compose ps db

# データベースログを確認
docker-compose logs db
```

## ライセンス

MIT
