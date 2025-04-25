from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security import HTTPBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
import os
import logging
from pathlib import Path
from app.auth.routes import router as auth_router
from app.database import init_db, close_db
from app.config import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI application with comprehensive settings
app = FastAPI(
    title="Budg API",
    description="API for Budg - A Personal Budget Management Application",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    # Add security schemes
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication and authorization endpoints",
        },
        {
            "name": "users",
            "description": "User management endpoints",
        },
    ],
)

# Add rate limiter to the app
app.state.limiter = limiter

# Fix rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests"},
    )

# Configure CORS with more specific settings
origins = [
    "https://localhost:3000",  # React dev server
    "http://localhost:3000",   # React dev server (non-HTTPS)
    "https://budg.app",        # Production domain
    "https://www.budg.app",    # Production domain with www
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Encoding",
        "Authorization",
        "Content-Type",
        "Origin",
        "X-Requested-With",
        "X-CSRF-Token",
    ],
    expose_headers=[
        "Content-Range",
        "X-Total-Count",
        "X-Error-Message",
    ],
    max_age=600,  # 10 minutes
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "budg.app", "www.budg.app"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add HTTPS redirect middleware
app.add_middleware(HTTPSRedirectMiddleware)

# Include auth routes
app.include_router(auth_router)

# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Welcome to Budg API"}

@app.on_event("startup")
async def on_startup():
    # Initialize database
    await init_db()
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def on_shutdown():
    # Close database connections
    await close_db()
    logger.info("Application shutdown complete")

if __name__ == "__main__":
    # Get the path to the SSL certificates
    cert_path = Path(__file__).parent.parent.parent / "certs"
    ssl_keyfile = cert_path / "localhost.key"
    ssl_certfile = cert_path / "localhost.crt"

    # Run the server with SSL
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=str(ssl_keyfile),
        ssl_certfile=str(ssl_certfile),
        reload=True,
        log_level="info",
        timeout_keep_alive=30,
    )
