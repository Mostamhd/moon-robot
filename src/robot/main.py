from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.robot.api.v1.router import api_router
from src.robot.core.config import settings
from src.robot.core.logging import setup_logging
from src.robot.services.database import engine
from src.robot.services.init_db import init_db as initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events"""
    # Startup
    setup_logging()
    # Initialize database with default data
    await initialize_database()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Moon Robot API",
    description="API for controlling a robot on the Moon",
    version="1.0.0",
    lifespan=lifespan,
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
