"""
Error Handlers

This module defines handlers for the custom exceptions defined in the template plugin.
These handlers can be used to format error responses in a consistent way.
"""

import logging
from typing import Dict, Any

from fastapi import Request
from fastapi.responses import JSONResponse

from template_plugin.errors.exceptions import (
    TemplateError,
    TemplateNotFoundError,
    TemplateExecutionError,
    TemplateProcessingError,
    TemplateValidationError,
    ClientInitializationError,
    ConnectionError,
    FileAccessError,
    AuthenticationError,
    AuthorizationError
)

logger = logging.getLogger("error-handlers")


async def template_error_handler(request: Request, exc: TemplateError) -> JSONResponse:
    """
    Handle TemplateError and its subclasses.
    
    Args:
        request: FastAPI request
        exc: Exception instance
        
    Returns:
        JSON response with error details
    """
    error_type = exc.__class__.__name__
    status_code = _get_status_code(exc)
    
    error_response = {
        "error": error_type,
        "message": str(exc),
        "status_code": status_code
    }
    
    logger.error(f"Template error: {error_type} - {str(exc)}")
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


def _get_status_code(exc: TemplateError) -> int:
    """
    Get the appropriate HTTP status code for an exception.
    
    Args:
        exc: Exception instance
        
    Returns:
        HTTP status code
    """
    if isinstance(exc, TemplateNotFoundError):
        return 404  # Not Found
    elif isinstance(exc, TemplateValidationError):
        return 400  # Bad Request
    elif isinstance(exc, AuthenticationError):
        return 401  # Unauthorized
    elif isinstance(exc, AuthorizationError):
        return 403  # Forbidden
    elif isinstance(exc, ConnectionError):
        return 502  # Bad Gateway
    elif isinstance(exc, FileAccessError):
        return 500  # Internal Server Error
    elif isinstance(exc, TemplateExecutionError):
        return 500  # Internal Server Error
    elif isinstance(exc, TemplateProcessingError):
        return 500  # Internal Server Error
    elif isinstance(exc, ClientInitializationError):
        return 500  # Internal Server Error
    else:
        return 500  # Internal Server Error


def setup_exception_handlers(app) -> None:
    """
    Set up exception handlers for a FastAPI application.
    
    Args:
        app: FastAPI application
    """
    app.add_exception_handler(TemplateError, template_error_handler)
    
    # You can add more specific handlers here if needed
    # app.add_exception_handler(TemplateNotFoundError, not_found_handler)
