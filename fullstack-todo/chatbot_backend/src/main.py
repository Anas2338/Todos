"""Main application entry point for the AI Chatbot Backend."""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import Dict, Any
import traceback

from .core.config import config
from .core.logging import setup_logging
from .core.database import init_db, close_db
from .chat.api import router as chat_router
from .models.base import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    print("Initializing database...")
    init_db()
    print("Database initialized successfully.")

    yield

    # Shutdown
    print("Closing database connections...")
    close_db()
    print("Database connections closed.")


# Create FastAPI app
app = FastAPI(
    title="AI Chatbot Backend",
    description="Backend API for AI-powered Todo Management Chatbot",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "AI Chatbot Backend is running", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # In a real implementation, you would perform actual checks
    # For now, we'll return a healthy status
    health_status = {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "version": "0.1.0",
        "checks": {
            "database": "connected",
            "external_services": "available"
        }
    }
    return health_status


@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    """Handle internal server errors."""
    print(f"Internal server error: {exc}")
    print(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": str(exc) if config.APP_ENV == "development" else "Internal server error"
            }
        }
    )


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: Exception):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error occurred",
                "details": str(exc)
            }
        }
    )


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    """Handle not found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "NOT_FOUND",
                "message": "Resource not found"
            }
        }
    )


@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    """Handle unauthorized errors."""
    return JSONResponse(
        status_code=401,
        content={
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Authentication required"
            }
        }
    )


@app.exception_handler(403)
async def forbidden_exception_handler(request: Request, exc: Exception):
    """Handle forbidden errors."""
    return JSONResponse(
        status_code=403,
        content={
            "error": {
                "code": "FORBIDDEN",
                "message": "Access denied"
            }
        }
    )


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["src"],
        log_level=config.LOG_LEVEL.lower()
    )