# Excel Web Service

## Overview (WHY)

Excel処理機能を提供するWebサービス。
ユーザー認証（JWT）を実装し、将来的にExcelファイルのアップロード・処理・ダウンロード機能を提供する。
現在はMVP開発フェーズ。

## Tech Stack (WHAT)

**Backend:**
- Python 3.14.0 (uv package manager)
- FastAPI + Uvicorn
- PostgreSQL 16
- SQLAlchemy (ORM)
- JWT Authentication (python-jose + passlib)

**Frontend:**
- Bun (runtime & package manager)
- React 19 + TypeScript 5
- Vite 7
- Tailwind CSS 4 + shadcn/ui
- sonner (toast notifications)

**Infrastructure:**
- Docker + Docker Compose
- PostgreSQL port: 5434 (local)

## Project Structure (WHAT)

```
/
├── app/                    # FastAPI backend
│   ├── api/endpoints/      # API endpoints
│   ├── repositories/       # DB access layer (pure data operations)
│   ├── services/           # Business logic layer
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── core/               # Config & security
│   └── database.py         # DB connection
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts (Auth)
│   │   ├── services/       # API client
│   │   └── types/          # TypeScript types
│   └── dist/               # Build output (gitignored)
├── main.py                 # FastAPI entry point
├── docker-compose.yml
└── .mcp.json               # MCP servers (serena, postgres)
```

**Architecture Pattern:**
- repositories: Pure DB operations (no business logic)
- services: Business logic, validation, orchestration
- API endpoints: Request/response handling only

## How to Work (HOW)

### Backend Development

**Start services:**
```bash
docker-compose up -d
```

**Add Python dependencies:**
Edit `pyproject.toml` dependencies array, then:
```bash
docker-compose up -d --build
```

**Check logs:**
```bash
docker-compose logs -f app
```

**Database access:**
```bash
docker-compose exec db psql -U postgres -d excel_web_service
```

### Frontend Development

**Start dev server:**
```bash
cd frontend
bun install  # First time only
bun run dev  # Opens on http://localhost:5173
```

**Add dependencies:**
```bash
cd frontend
bun add <package-name>
```

**Build for production:**
```bash
cd frontend
bun run build  # Output to frontend/dist/
```

### Testing Changes

1. Backend: Access http://localhost:8000/docs (Swagger UI)
2. Frontend: Access http://localhost:5173 (Vite dev server)
3. Check Docker logs for errors
4. Ensure tests pass before committing (when added)

## API Endpoints

Current endpoints:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Login (returns JWT)
- `GET /api/auth/me` - Get current user (requires auth)
- `GET /health` - Health check

## Important Notes

### Code Style
- Follow existing code patterns in the codebase
- Backend: Use type hints, docstrings in Japanese
- Frontend: Use TypeScript strict mode, functional components

### Authentication
- JWT tokens stored in localStorage
- Token included in Authorization header: `Bearer <token>`
- Auth context manages global auth state

### Database
- Auto-creates tables on startup via `Base.metadata.create_all()`
- Migrations: Alembic (not yet configured)
- Connection string: `postgresql://postgres:postgres@localhost:5434/excel_web_service`

### When Making Changes
1. Read existing code in the relevant area first
2. Follow the repositories → services → endpoints pattern
3. Update both backend AND frontend if API changes
4. Test manually via Swagger UI and frontend
5. Commit with descriptive messages in Japanese

## Additional Documentation

For detailed information, refer to:
- `README.md` - Full setup instructions
- `.env.example` - Environment variables template
- `frontend/.env.example` - Frontend environment variables

## MCP Servers Available

- **serena**: Project management (configured in `.mcp.json`)
- **postgres**: Direct database queries (configured in `.mcp.json`)

Use `@serena` or `@postgres` to interact with these tools.
