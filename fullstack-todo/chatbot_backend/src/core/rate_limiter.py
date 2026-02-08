"""Rate limiting middleware for chat endpoints."""

import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import HTTPException, Request
from .config import config
from uuid import UUID


class RateLimiter:
    """Simple in-memory rate limiter for chat endpoints."""

    def __init__(self):
        # Dictionary to store request timestamps per user: {user_id: [timestamps]}
        self.requests: Dict[UUID, list] = defaultdict(list)

    def is_allowed(self, user_id: UUID) -> Tuple[bool, int, int]:
        """
        Check if the user is allowed to make a request.

        Returns:
            - bool: Whether the request is allowed
            - int: Remaining requests in the current window
            - int: Seconds until the rate limit resets
        """
        now = time.time()
        window_start = now - 3600  # 1 hour window in seconds

        # Clean old requests outside the window
        if user_id in self.requests:
            self.requests[user_id] = [
                timestamp for timestamp in self.requests[user_id]
                if timestamp > window_start
            ]

        # Get current request count
        current_requests = len(self.requests[user_id])

        # Check if we're under the limit
        if current_requests < config.RATE_LIMIT_REQUESTS_PER_HOUR:
            # Add current request
            self.requests[user_id].append(now)
            remaining = config.RATE_LIMIT_REQUESTS_PER_HOUR - current_requests - 1

            # Calculate reset time (in seconds)
            if self.requests[user_id]:
                oldest_request = min(self.requests[user_id])
                reset_time = int(oldest_request + 3600 - now)
            else:
                reset_time = 3600

            return True, max(0, remaining), max(0, reset_time)

        # Calculate reset time (in seconds)
        oldest_request = min(self.requests[user_id])
        reset_time = int(oldest_request + 3600 - now)

        return False, 0, max(0, reset_time)


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(request: Request, user_id: UUID) -> None:
    """Check if the user has exceeded the rate limit."""
    is_allowed, remaining, reset_time = rate_limiter.is_allowed(user_id)

    # Add rate limit headers to response
    request.state.rate_limit_remaining = remaining
    request.state.rate_limit_reset = reset_time

    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": {
                    "code": "TOO_MANY_REQUESTS",
                    "message": f"Rate limit exceeded. {config.RATE_LIMIT_REQUESTS_PER_HOUR} requests per hour allowed.",
                    "details": f"Try again in {reset_time} seconds"
                }
            }
        )