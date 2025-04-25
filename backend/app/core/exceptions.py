from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BudgException(HTTPException):
    """Base exception for Budg application"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BudgException):
    """Resource not found exception"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class ValidationException(BudgException):
    """Validation error exception"""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

class AuthenticationException(BudgException):
    """Authentication error exception"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationException(BudgException):
    """Authorization error exception"""
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ConflictException(BudgException):
    """Resource conflict exception"""
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

class RateLimitException(BudgException):
    """Rate limit exceeded exception"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail
        )

class DatabaseException(BudgException):
    """Database operation exception"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
