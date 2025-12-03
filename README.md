# Excel Web Service

FastAPIを使用したExcel処理Webサービス

## 開発環境セットアップ

### 必要なもの
- Docker & Docker Compose

### セットアップ手順

1. 環境変数ファイルをコピー
```bash
cp .env.example .env
```

2. Docker環境を起動（初回はビルドに時間がかかります）
```bash
docker-compose up -d --build
```

3. FastAPIサーバーを起動
```bash
docker-compose exec app uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. ブラウザでアクセス
```
http://localhost:8000
```

FastAPIのドキュメント（Swagger UI）：
```
http://localhost:8000/docs
```

## 開発フロー

### コード編集
ローカルでファイルを編集すると、サーバー起動中であれば自動的にリロードされます（`--reload`オプション有効時）。

### パッケージ追加

1. コンテナ内でパッケージを追加
```bash
docker-compose exec app uv pip install <パッケージ名>
```

2. `pyproject.toml`に追記（永続化）
```toml
[project]
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "新しいパッケージ>=バージョン",
]
```

3. コンテナを再ビルド
```bash
docker-compose up -d --build
```

### ログ確認
```bash
# 全てのログ
docker-compose logs -f

# アプリケーションのみ
docker-compose logs -f app

# データベースのみ
docker-compose logs -f db
```

### データベース管理
```bash
# PostgreSQLに接続
docker-compose exec db psql -U postgres -d excel_web_service

# データベースのバックアップ
docker-compose exec db pg_dump -U postgres excel_web_service > backup.sql

# データベースのリストア
docker-compose exec -T db psql -U postgres excel_web_service < backup.sql
```

### コンテナ操作
```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# 停止（ボリュームも削除）
docker-compose down -v

# 再起動
docker-compose restart

# appコンテナに入る
docker-compose exec app bash

# FastAPIサーバーを起動
docker-compose exec app uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# その他のコマンド実行例
docker-compose exec app python -m pytest
docker-compose exec app uv pip list
```

## プロジェクト構成

```
.
├── app/                     # FastAPIアプリケーション
│   ├── api/                 # APIエンドポイント
│   │   ├── endpoints/       # 各エンドポイント
│   │   └── router.py        # ルーター統合
│   ├── core/                # 設定・セキュリティ
│   ├── models/              # DBモデル
│   ├── repositories/        # データアクセス層
│   ├── schemas/             # Pydanticスキーマ
│   ├── services/            # ビジネスロジック
│   └── database.py          # DB接続設定
├── frontend/                # Reactフロントエンド
│   ├── src/                 # ソースコード
│   ├── public/              # 静的ファイル
│   └── dist/                # ビルド成果物
├── Dockerfile               # Python 3.14環境の定義
├── docker-compose.yml       # app + db の構成
├── .dockerignore            # Dockerビルドから除外するファイル
├── .env                     # 環境変数（Git管理外）
├── .env.example             # 環境変数サンプル
├── pyproject.toml           # Python依存パッケージ（uv管理）
├── main.py                  # FastAPIエントリーポイント
└── README.md                # このファイル
```

## データベース接続情報

### Docker内から接続（アプリケーションから）
```python
DATABASE_URL = "postgresql://postgres:postgres@db:5432/excel_web_service"
```

### ローカルから接続（DB管理ツールなど）
- Host: localhost
- Port: 5432
- User: postgres
- Password: postgres
- Database: excel_web_service

## フロントエンド開発

### 開発サーバーの起動

1. フロントエンドディレクトリに移動
```bash
cd frontend
```

2. 依存関係のインストール（初回のみ）
```bash
bun install
```

3. 開発サーバーを起動
```bash
bun run dev
```

4. ブラウザでアクセス
```
http://localhost:5173
```

### 本番ビルド

```bash
cd frontend
bun run build
```

ビルド成果物は `frontend/dist/` に出力されます。
FastAPIが自動的に配信するため、追加の設定は不要です。

### フロントエンド構成

```
frontend/
├── src/           # Reactソースコード
├── public/        # 静的ファイル
├── dist/          # ビルド成果物（gitignore）
├── package.json
└── vite.config.ts
```

## 技術スタック

### バックエンド
- **Python**: 3.14.0
- **パッケージマネージャー**: uv
- **Webフレームワーク**: FastAPI
- **ASGIサーバー**: Uvicorn
- **データベース**: PostgreSQL 16
- **ORM**: SQLAlchemy
- **認証**: JWT (python-jose + passlib)
- **コンテナ**: Docker / Docker Compose

### フロントエンド
- **ランタイム**: Bun
- **フレームワーク**: React 19
- **ビルドツール**: Vite 7
- **言語**: TypeScript 5

## トラブルシューティング

### ポートが既に使用されている
```bash
# 8000番ポートを使用しているプロセスを確認
lsof -i :8000

# .envでポートを変更
# docker-compose.ymlの ports を "${APP_PORT}:8000" に変更
```

### コンテナが起動しない
```bash
# ログを確認
docker-compose logs

# 完全にクリーンアップして再ビルド
docker-compose down -v
docker-compose up -d --build
```

### パッケージが反映されない
```bash
# キャッシュなしで再ビルド
docker-compose build --no-cache
docker-compose up -d
```

## IDE設定（VSCode）

Remote - Containersを使用してコンテナ内で開発する場合：

1. VSCodeの拡張機能「Dev Containers」をインストール
2. コマンドパレット（Cmd+Shift+P）から「Dev Containers: Attach to Running Container」
3. `excel-app`を選択
4. コンテナ内でVSCodeが開きます
