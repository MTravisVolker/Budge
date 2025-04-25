from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.rate_limiter import rate_limiter

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        # Check rate limits
        await rate_limiter.check_rate_limit(request)

        # Process request
        response = await call_next(request)
        return response
