"""
Template Plugin Errors Package

This package provides error handling and exceptions for the template plugin.
"""

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
    AuthorizationError,
    BackstageAPIError
)

__all__ = [
    'TemplateError',
    'TemplateNotFoundError',
    'TemplateExecutionError',
    'TemplateProcessingError',
    'TemplateValidationError',
    'ClientInitializationError',
    'ConnectionError',
    'FileAccessError',
    'AuthenticationError',
    'AuthorizationError',
    'BackstageAPIError'
]
