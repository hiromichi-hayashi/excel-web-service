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
- **フレームワーク**: React 18
- **ビルドツール**: Vite 5
- **言語**: TypeScript
- **構成**: Laravel風（backend/frontend/ 内で管理）

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

#### 4. フロントエンド（React + Vite）の起動

フロントエンドはローカルのNode.js 22.18.0環境で実行します：

```bash
cd backend/frontend
npm install
npm run dev
```

フロントエンドは `http://localhost:3000` で起動します。

**開発時の構成:**
- フロントエンド: Vite dev server (3000)
- バックエンドAPI: FastAPI (8000)
- Viteの proxy設定により `/api` へのリクエストは自動的にFastAPIに転送されます

**本番ビルド:**

```bash
cd backend/frontend
npm run build
```

ビルドされたファイルは `backend/app/static/` に出力され、FastAPIが配信します。

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

### フロントエンド

```bash
# 開発サーバー起動（ホットリロード有効）
cd backend/frontend
npm run dev

# 本番ビルド
npm run build

# ビルドのプレビュー
npm run preview

# リンター実行
npm run lint

# 依存パッケージの更新
npm update
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
├── backend/                        # バックエンド（MVP向けシンプル構造）
│   ├── app/                       # FastAPIアプリケーション
│   │   ├── __init__.py
│   │   ├── main.py                # メインエントリーポイント
│   │   ├── api/                   # APIルーティング
│   │   │   ├── deps.py           # 依存性注入
│   │   │   ├── api.py            # ルーター集約
│   │   │   └── endpoints/        # エンドポイント（機能ごとに追加）
│   │   │       ├── health.py     # ヘルスチェック
│   │   │       └── info.py       # API情報
│   │   ├── core/                 # コア機能
│   │   │   └── config.py        # 設定管理（Pydantic Settings）
│   │   ├── db/                   # データベース
│   │   │   ├── base.py          # SQLAlchemy Base
│   │   │   └── session.py       # セッション管理
│   │   ├── models/               # SQLAlchemyモデル（必要時に追加）
│   │   ├── schemas/              # Pydanticスキーマ（必要時に追加）
│   │   ├── services/             # ビジネスロジック（拡張性確保）
│   │   └── static/               # ビルド済みフロントエンド（本番環境）
│   ├── frontend/                  # フロントエンドソース（Laravel風）
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   └── ...
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   ├── tests/                     # テスト
│   │   ├── conftest.py           # pytest設定
│   │   └── test_api.py
│   ├── alembic/                   # DBマイグレーション
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── Dockerfile                 # Dockerイメージ定義
│   └── requirements.txt           # Python依存パッケージ
├── docker-compose.yml             # Docker Compose設定
├── .env.example                   # 環境変数のサンプル
├── .gitignore                     # Git除外設定
└── README.md                      # このファイル
```

**構造の特徴:**
- **MVP向けシンプル設計**: バージョニングなし、必要最小限の構成
- **拡張性確保**: services/, models/, schemas/ は必要時に追加
- **モノレポ構成**: backend/frontend/ でフロントエンドを同居管理

**開発環境:**
- フロントエンド: `backend/frontend/` でVite開発サーバー（localhost:3000）
- バックエンド: Dockerコンテナで FastAPI（localhost:8000）
- API: `/api/` プレフィックス（例: `/api/health`, `/api/info`）
- 設定: `app/core/config.py` で環境変数を型安全に管理

**本番環境:**
- `npm run build` → `backend/app/static/` に出力
- FastAPIが静的ファイル配信（1コンテナで完結）
- Alembicでデータベースマイグレーション管理

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

### フロントエンドのビルドエラー

```bash
# node_modulesを削除して再インストール
cd backend/frontend
rm -rf node_modules package-lock.json
npm install

# Node.jsのバージョン確認（22.18.0であること）
node --version
```

### APIリクエストが失敗する

開発時は Vite の proxy 設定により `/api` へのリクエストが `http://localhost:8000` に転送されます。

- バックエンドが起動しているか確認: `docker-compose ps backend`
- ポート8000が空いているか確認: `curl http://localhost:8000/health`

## ライセンス

MIT
