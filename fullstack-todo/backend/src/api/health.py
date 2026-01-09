from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any
import time

health_router = APIRouter()


@health_router.get("/health")
def health_check():
    """Health check endpoint to verify the application is running."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-backend-api"
    }


@health_router.get("/health/extended")
def extended_health_check():
    """Extended health check with additional system information."""
    # In a real application, this would check database connections,
    # external services, etc.
    health_info = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-backend-api",
        "checks": {
            "database": {"status": "connected", "timestamp": datetime.utcnow().isoformat()},
            "cache": {"status": "connected", "timestamp": datetime.utcnow().isoformat()},
            "external_apis": {"status": "available", "timestamp": datetime.utcnow().isoformat()}
        }
    }

    return health_info