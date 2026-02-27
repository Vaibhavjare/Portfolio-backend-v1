# main.py

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db, close_db
from app.core.config import settings

# Routers
from app.routers.project_router import router as project_router
from app.routers.skill_router import router as skill_router
from app.routers.auth_router import router as auth_router
from app.routers.certification_router import router as certificate_router
from app.routers.contact_router import router as contact_router
from app.routers.profile_router import router as profile_router


# =========================================
# Logging Configuration
# =========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger("portfolio-api")


# =========================================
# Lifespan (Startup & Shutdown)
# =========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("🚀 Application startup complete")
        yield
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    finally:
        await close_db()
        logger.info("🔒 Application shutdown complete")


# =========================================
# FastAPI Initialization
# =========================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Portfolio Backend API (Public + Admin Panel)",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# =========================================
# CORS Configuration
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# Register Routers (NO PREFIX)
# =========================================

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(project_router)
app.include_router(skill_router)
app.include_router(certificate_router)
app.include_router(contact_router)


# =========================================
# Root Endpoint
# =========================================

@app.get("/", tags=["Public"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
    }


# =========================================
# Health Check
# =========================================

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
    }