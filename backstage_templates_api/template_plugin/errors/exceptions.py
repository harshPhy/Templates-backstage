"""
Template Plugin Exceptions

This module defines custom exceptions used throughout the template plugin.
"""


class TemplateError(Exception):
    """Base exception for template-related errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class TemplateNotFoundError(TemplateError):
    """Exception raised when a template is not found."""
    pass


class TemplateExecutionError(TemplateError):
    """Exception raised when there is an error executing a template."""
    pass


class TemplateProcessingError(TemplateError):
    """Exception raised when there is an error processing template files."""
    pass


class TemplateValidationError(TemplateError):
    """Exception raised when template parameters fail validation."""
    pass


class ClientInitializationError(TemplateError):
    """Exception raised when there is an error initializing a template client."""
    pass


class ConnectionError(TemplateError):
    """Exception raised when there is a connection error with a template source."""
    pass


class FileAccessError(TemplateError):
    """Exception raised when there is an error accessing a file."""
    pass


class AuthenticationError(TemplateError):
    """Exception raised when there is an authentication error."""
    pass


class AuthorizationError(TemplateError):
    """Exception raised when there is an authorization error."""
    pass


class BackstageAPIError(TemplateError):
    """Exception raised when there is an error with the Backstage API."""
    pass
