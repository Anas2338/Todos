from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get rate limit from environment, default to 100 per hour
RATE_LIMIT = os.getenv("RATE_LIMIT", "100/hour")

# Initialize the limiter
limiter = Limiter(key_func=get_remote_address)

def setup_rate_limiting(app: FastAPI):
    """Set up rate limiting for the FastAPI application."""
    # Attach the limiter to the app
    app.state.limiter = limiter
    # Add the rate limit exceeded handler
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def limit_request():
    """Decorator to apply rate limiting to a route."""
    return limiter.limit(RATE_LIMIT)