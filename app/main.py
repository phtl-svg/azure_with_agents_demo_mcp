# (c) Danit Consultancy and Development, January-2026, danittech@yahoo.com
# Usage:  make dev
# Then, access the API via:
# - API Documentation: http://localhost:8000/docs
# - Health Check: http://localhost:8000/health
# - Agent Endpoint: http://localhost:8000/api/v1/agent/invoke
# Architecture:
# Client Request → FastAPI → LangGraph Agent → MCP Tools → External Services
#                     ↓           ↓                ↓
#                  Logging    State Mgmt     Tool Registry

""" FastAPI application entry point """

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)

# ----------------------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    # Create all database tables that don't exist yet.
    # Base.metadata.create_all() reads every model registered under Base
    # (currently just Document) and issues CREATE TABLE IF NOT EXISTS.
    # This means the first startup against a fresh database is safe —
    # no manual migration step needed for development.
    from app.db.session import engine
    from app.db.models import Base
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("database_connected")
    except Exception as e:
        # Database is unavailable (not configured, deleted, or unreachable).
        # The app starts anyway — endpoints that don't use the DB keep working.
        # search_documents will return "no results" rather than crashing.
        logger.warning("database_unavailable", error=str(e))
    logger.info("application_starting", environment=settings.ENVIRONMENT)
    yield
    logger.info("application_shutting_down")

# ----------------------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Agent with FastAPI, LangGraph, and MCP",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# ----------------------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
        }
    )

@app.get("/")
async def root():
    return {
        "message": "AI Agent API",
        "docs": "/docs",
        "version": "0.1.0",
    }
