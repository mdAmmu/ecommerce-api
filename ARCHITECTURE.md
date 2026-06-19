# Architecture

Directory layout for the `app/` package.

| Folder | Purpose |
|---|---|
| `api/` | Route definitions organized per feature. Each module registers a FastAPI router. |
| `core/` | App-wide configuration, security utilities, and constants. |
| `db/` | Database engine, session factory, and connection lifecycle management. |
| `models/` | SQLAlchemy ORM table models. |
| `schemas/` | Pydantic models for request validation and response serialization. |
| `services/` | Business logic layer. Orchestrates repositories and enforces domain rules. |
| `repositories/` | All database queries. Each module owns queries for one aggregate/table. |
| `middleware/` | Custom request/response middleware (logging, timing, CORS overrides, etc.). |
| `dependencies/` | FastAPI injectable dependencies (current user, DB session, pagination, etc.). |
| `utils/` | Small, stateless helper functions shared across the codebase. |
| `tests/` | All test files, mirroring the `app/` structure. |
| `migrations/` | Alembic migration scripts and configuration. |
