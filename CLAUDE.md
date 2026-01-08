# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**大噜农场展示系统** (Dalu Farm Display System) - A farm management dashboard displaying crops, animals, and flowers data with charts.

**Tech Stack:**
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: Vue 3 + TypeScript + Pinia + ECharts
- Deployment: Docker Compose

---

## Development Commands

### Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild after dependency changes
docker-compose build backend
docker-compose build frontend
```

### Backend (Local Development)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Local Development)
```bash
cd frontend
pnpm install
pnpm run dev
```

### Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && pnpm run test
```

---

## Architecture

### Backend Structure
```
backend/app/
├── main.py           # FastAPI app entry, registers all routers
├── core/config.py    # Settings from env vars
├── db/
│   ├── base.py       # SQLAlchemy Base declarative
│   └── session.py    # get_db() dependency
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic request/response models
└── api/v1/           # API route handlers
```

**Key Pattern:** Routes use Pydantic schemas for request/response, models are SQLAlchemy ORM classes. Both define enums but separately.

### Frontend Structure
```
frontend/src/
├── api/              # API client functions (no state)
├── stores/           # Pinia stores (state + api calls)
├── types/            # TypeScript interfaces/mirrors of backend schemas
├── router/           # Vue Router config
└── views/            # Page components
```

**Key Pattern:**
- `api/` - Pure API callers using axios, return typed responses
- `stores/` - Wrap API calls, manage loading/error states, cache data
- `types/` - Mirror backend Pydantic schemas (enums must match)

### API Endpoints
All prefixed with `/api/v1/`:
- `GET/POST /crops` - List/create crops
- `GET/PUT/DELETE /crops/{id}` - Crop CRUD
- `PATCH /crops/{id}/harvest` - Mark as harvested
- `GET/POST /animals` - List/create animals
- `GET/PUT/DELETE /animals/{id}` - Animal CRUD
- `GET/POST /flowers` - List/create flowers
- `GET/PUT/DELETE /flowers/{id}` - Flower CRUD
- `GET /statistics/overview` - Summary stats
- `GET /statistics/charts` - Chart data for ECharts
- `GET /statistics/calendar` - Calendar events

### Data Models

**Crop:** name, variety, area, plant_date, expected_harvest_date, actual_harvest_date, total_yield, unit, status (growing/harvested/failed)

**Animal:** name, variety, quantity, acquire_date, product_type, estimated_daily_yield, yield_unit

**Flower:** name, variety, quantity, plant_date, bloom_season, colors (JSON), purpose, estimated_yield

**YieldRecord:** crop_id (FK), record_date, quantity, unit, area_harvested

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| POSTGRES_USER | dalu | Database user |
| POSTGRES_PASSWORD | dalu_password | Database password |
| POSTGRES_DB | dalu_farm | Database name |
| BACKEND_PORT | 8000 | Backend port |
| FRONTEND_PORT | 5173 | Frontend port |
| CORS_ORIGINS | http://localhost:5173 | Allowed origins |
| REQUIRE_AUTH | false | Enable auth for writes |
| VITE_API_URL | http://localhost:8000/api/v1 | Backend URL from frontend |

---

## Conventions

### Backend
- Use Pydantic `model_dump(exclude_unset=True)` for partial updates
- Use HTTP 204 for DELETE responses
- Use `status.HTTP_201_CREATED` for POST creation
- Enums defined in both `models/` and `schemas/` - keep in sync

### Frontend
- Use `<script setup lang="ts">` for Vue 3 components
- Use Pinia stores with composition API style
- API error handling: `err.response?.data?.detail`
- Chart components use ECharts directly (no wrapper library)

### Git Workflow
- Feature branches: `feature/xxx`, `bugfix/xxx`
- Use `/commit` to create commits (semi-automated)
- Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`
- Chinese commit messages acceptable for this project

---

## Known Issues / TODO

- Database migrations (Alembic) not yet configured
- Authentication (JWT) scaffolded but not implemented (`REQUIRE_AUTH=false`)
- Frontend chart components need responsive resize handling
- Test files not yet written
