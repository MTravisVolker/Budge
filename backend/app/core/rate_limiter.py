from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis import Redis
from typing import Optional
import time
from app.config import get_settings

settings = get_settings()

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.bearer = HTTPBearer()

    async def get_user_id_from_token(self, request: Request) -> Optional[str]:
        """Extract user ID from JWT token"""
        try:
            credentials: HTTPAuthorizationCredentials = await self.bearer(request)
            if not credentials:
                return None
            # In a real implementation, you would decode the JWT and get the user ID
            # For now, we'll use the token itself as a unique identifier
            return credentials.credentials
        except Exception:
            return None

    def get_ip_key(self, request: Request) -> str:
        """Get IP address from request"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host

    async def check_rate_limit(self, request: Request) -> None:
        """Check if request should be rate limited"""
        # Get user ID from token if available
        user_id = await self.get_user_id_from_token(request)

        # Check user-based rate limit
        if user_id:
            user_key = f"rate_limit:user:{user_id}"
            if not await self._check_key(user_key, settings.RATE_LIMIT_USER):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="User rate limit exceeded"
                )

        # Check IP-based rate limit
        ip_key = f"rate_limit:ip:{self.get_ip_key(request)}"
        if not await self._check_key(ip_key, settings.RATE_LIMIT_IP):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="IP rate limit exceeded"
            )

    async def _check_key(self, key: str, limit: int) -> bool:
        """Check if a key has exceeded its rate limit"""
        current = self.redis.get(key)
        if current is None:
            self.redis.setex(key, 60, 1)  # 1 request, expires in 60 seconds
            return True

        current = int(current)
        if current >= limit:
            return False

        self.redis.incr(key)
        return True

# Create a singleton instance
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)
rate_limiter = RateLimiter(redis_client)
