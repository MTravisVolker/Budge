from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import BudgException
import logging
import traceback
from typing import Any, Callable
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self.handle_exception(request, exc)

    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle all exceptions and return appropriate JSON response"""

        # Log the error
        logger.error(
            f"Error processing request {request.method} {request.url.path}: {str(exc)}",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc()
            }
        )

        # Handle specific exceptions
        if isinstance(exc, BudgException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "code": exc.status_code,
                        "message": exc.detail,
                        "type": type(exc).__name__
                    }
                },
                headers=exc.headers if hasattr(exc, "headers") else None
            )
        elif isinstance(exc, RequestValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": {
                        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                        "message": "Validation error",
                        "type": "ValidationError",
                        "details": exc.errors()
                    }
                }
            )
        elif isinstance(exc, SQLAlchemyError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "Database error occurred",
                        "type": "DatabaseError"
                    }
                }
            )
        else:
            # Handle unexpected errors
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "An unexpected error occurred",
                        "type": "UnexpectedError"
                    }
                }
            )
