import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

def setup_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """Configure logging for the application"""

    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Create formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
        'Request: %(request_method)s %(request_path)s\n'
        'Error Type: %(error_type)s\n'
        'Error Message: %(error_message)s\n'
        'Traceback: %(traceback)s\n'
    )

    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # Configure file handler if log file is specified
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(level)
        root_logger.addHandler(file_handler)

    # Configure SQLAlchemy logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # Configure third-party library logging
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('fastapi').setLevel(logging.WARNING)
