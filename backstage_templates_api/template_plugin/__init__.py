"""
Backstage Templates API Plugin

This module provides a plugin for interacting with templates from various sources.
The main functionality is exposed through the TemplatePlugin class.
"""

from template_plugin.template_plugin import TemplatePlugin
from template_plugin.clients.base_client import BaseClient
from template_plugin.clients.backstage import BackstageClient
from template_plugin.clients.local import LocalClient
from template_plugin.models.template_models import TemplateTask, TemplateTaskResponse
from template_plugin.errors.exceptions import TemplateError, TemplateNotFoundError

__all__ = [
    'TemplatePlugin',
    'BaseClient',
    'BackstageClient',
    'LocalClient',
    'TemplateTask',
    'TemplateTaskResponse',
    'TemplateError',
    'TemplateNotFoundError',
]
