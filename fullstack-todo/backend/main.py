import sys
import os
# Add the src directory to the Python path to make imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth_routes import auth_router
from api.task_routes import task_router
from api.health import health_router
from api.error_handlers import setup_error_handlers
from utils.rate_limiter import setup_rate_limiting
import uvicorn

app = FastAPI(
    title="Todo API",
    description="A secure, multi-user Todo API backend with authentication",
    version="1.0.0"
)

# Setup rate limiting
setup_rate_limiting(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Include API routes
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(health_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)