<p align="center">
  <img src="assets/logo.png" alt="FastAPI Template Logo" width="200" />
</p>

<h1 align="center">FastAPI Template</h1>

<p align="center">
  Modular, type-safe FastAPI starter with PostgreSQL, Redis, Alembic, tests, and linters.
</p>

---

## 🚀 Idea & Philosophy

This project is more than “yet another FastAPI boilerplate” — it is a **skeleton for real services** that need to grow safely:

- **Clear separation of layers**:
  - `infra/` — infrastructure (DB, Redis, logger, migrations).
  - `modules/` — business functionality (each feature lives on its own).
- **Modular layout**:
  - Every module follows the same scaffold: `models/`, `schemas/`, `service/`, `router/`.
  - New features stay isolated instead of turning into spaghetti.
- **Safety & quality**:
  - `ruff` — linter + formatter.
  - `mypy` — static typing.
  - `pytest` — unit + integration tests.
- **Ready extension points**:
  - `health` module already available (checks PostgreSQL + Redis).
  - Preconfigured wiring with logger, DB, and cache.

---

## 📂 Project Structure

```bash
.
├── README.md
├── alembic/               # Database migrations (Alembic)
├── alembic.ini
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings / .env
│   ├── main.py            # create_app() + app
│   ├── infra/
│   │   ├── __init__.py
│   │   ├── cache/
│   │   │   └── redis.py   # Redis async client
│   │   ├── db/
│   │   │   └── postgres.py# SQLAlchemy async engine + Session + Base
│   │   └── logger/
│   │       └── logger.py  # Central logger
│   └── modules/
│       ├── __init__.py
│       └── health/
│           ├── models/    # (empty scaffold for now)
│           ├── router/    # /health endpoint
│           ├── schemas/   # HealthResponse
│           └── service/   # HealthService (Postgres + Redis check)
├── assets/
│   └── logo.png           # README logo
├── main.py                # Thin wrapper (optional)
├── pyproject.toml         # Dependencies & configs
├── pytest.ini             # Pytest configuration
├── scripts/
│   └── lint.sh            # Ruff + formatting + mypy
└── tests/
    ├── unit/              # Unit tests
    └── integration/       # Integration tests (/health)
```

---

## 🧠 Architecture Overview

### 1. `app/config.py` — settings

* Uses `pydantic-settings` to read configuration from `.env`.
* Key fields:

  * `APP_NAME`
  * `DEBUG`
  * `API_PREFIX` (`/api`, `/v1`, etc.)
  * `DATABASE_URL` — async PostgreSQL connection string (`postgresql+asyncpg://...`)
  * `REDIS_URL` — Redis connection string (`redis://...`)

```python
from app.config import get_settings

settings = get_settings()
print(settings.DATABASE_URL)
```

### 2. `app/infra/` — infrastructure

* `db/postgres.py`:

  * `Base` — declarative base (SQLAlchemy 2.x).
  * `engine` — async engine.
  * `SessionFactory` — `async_sessionmaker`.
  * `get_db_session()` — FastAPI dependency.

* `cache/redis.py`:

  * Lazy Redis client (singleton per process).
  * `get_redis_dep()` — dependency.
  * `check_redis()` — health check.

* `logger/logger.py`:

  * Unified `fastapi_template` logger.
  * Colorized output.
  * Harmonized format for `sqlalchemy.engine` logs.

### 3. `app/modules/` — feature modules

Example: `health`.

* `schemas/health_response.py` — Pydantic schema:

  ```python
  class HealthResponse(BaseModel):
      status: str     # ok / degraded
      postgres: str   # ok / fail
      redis: str      # ok / fail
  ```

* `service/health_service.py` — health-check logic:

  * `check_postgres(session: AsyncSession) -> bool`
  * `check_redis() -> bool`

* `router/health_router.py` — FastAPI router:

  * `GET /health/` → `HealthResponse`.

---

## ✨ Features

* ✅ **FastAPI** with async stack.
* ✅ **PostgreSQL** via `SQLAlchemy 2.x + asyncpg`.
* ✅ **Redis** via `redis.asyncio`.
* ✅ **Alembic** migrations.
* ✅ **Health check**:

  * `/health/` validates Postgres and Redis connectivity.
* ✅ **Logging**:

  * Shared logger,
  * unified output for app + SQLAlchemy logs.
* ✅ **Tests**:

  * `tests/unit` — unit tests for health service, config, logger.
  * `tests/integration` — integration test for `/health/`.
* ✅ **Code quality**:

  * `ruff` — lint + format.
  * `mypy` — type checking.
  * `pytest` — test runner.
  * `pytest-cov` — optional coverage.

---

## 🛠 Setup & Run

### 1. Requirements

* Python `>= 3.12`
* [`uv`](https://github.com/astral-sh/uv) (recommended)
  or any environment manager you prefer.

### 2. Install dependencies

```bash
# From the project root
uv sync
```

This creates `.venv` and installs everything from `pyproject.toml`.

### 3. Configure environment

Create `.env` in the root:

```env
APP_NAME="FastAPI Template"
DEBUG=true

DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
REDIS_URL="redis://localhost:6379/0"
API_PREFIX="/api"
```

Make sure PostgreSQL and Redis are running locally
(or adjust `DATABASE_URL` / `REDIS_URL`).

### 4. Migrations (Alembic)

Initialize DB (schema already created):

```bash
uv run alembic upgrade head
```

Create a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe changes"
uv run alembic upgrade head
```

### 5. Run the app

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Accessible at:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Health check: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## 🧪 Tests

### Run everything

```bash
uv run pytest
```

### Unit tests only

```bash
uv run pytest -m "not integration"
```

### Integration tests

```bash
uv run pytest -m integration
```

> Integration tests expect live PostgreSQL and Redis with valid `DATABASE_URL` and `REDIS_URL`.

---

## 🧹 Linters & Types

Use `scripts/lint.sh` to execute the full pipeline:

```bash
./scripts/lint.sh
```

It runs:

1. `uv run ruff check .` — linting.
2. `uv run ruff format .` — formatting.
3. `uv run mypy app tests` — static typing.

You can run steps separately:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy app tests
```

---

## 🧩 Add a New Module

Example for a `users` module:

1. Scaffold directories:

```bash
mkdir -p app/modules/users/{models,schemas,service,router}
touch app/modules/users/__init__.py
touch app/modules/users/models/__init__.py
touch app/modules/users/schemas/__init__.py
touch app/modules/users/service/__init__.py
touch app/modules/users/router/__init__.py
```

2. Define models in `models/` (inherit from `Base` in `infra/db/postgres.py`).
3. Add schemas (`schemas/`), services (`service/`), and routers (`router/`).
4. Wire the router in `app/main.py`:

```python
from app.modules.users.router.users_router import router as users_router

app.include_router(users_router, prefix=settings.API_PREFIX)
```

5. Create an Alembic migration if you add tables.
6. Write unit and integration tests under `tests/`.

---

## 📌 Wrap-up

This template delivers:

* A production-ready **FastAPI service skeleton**.
* Clear boundaries: infrastructure vs. business modules.
* Working integrations with PostgreSQL, Redis, Alembic.
* Quality tooling out of the box: **ruff**, **mypy**, **pytest**.

Next ideas:

* add new modules (auth, users, billing, analytics),
* plug into Docker/Kubernetes,
* extend observability (Prometheus, Sentry, etc.).

Start building features on top of this foundation 💙
