"""
LifeOps API — FastAPI Entrypoint
==================================
Central nervous system of the LifeOps application.
Combines personal (activities, sport, books, films) and
professional (projects, tasks) management in one API.

Run with:
    uvicorn main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routers.activities import router as activities_router
from routers.projects import router as projects_router, tasks_router
from routers.stats import router as stats_router

# ── App setup ─────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title="LifeOps API",
    version="0.1.0",
    description=(
        "🚀 LifeOps — Your personal & professional life dashboard. "
        "Full-stack app combining activity tracking (sport, books, films, learning) "
        "with project & task management. "
        "Built with FastAPI + Supabase for Datalaria."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ───────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ─────────────────────────────

app.include_router(activities_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(stats_router)


# ── Root & Health ─────────────────────────────────

@app.get("/", tags=["System"])
async def root():
    """API root — welcome message."""
    return {
        "app": "LifeOps API",
        "version": "0.1.0",
        "docs": "/docs",
        "status": "operational",
    }


@app.get("/health", tags=["System"])
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "engine": "LifeOps v0.1.0",
        "database": "Supabase (datalaria-core)",
        "schema": settings.supabase_schema,
    }


# ── Dev server ────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
