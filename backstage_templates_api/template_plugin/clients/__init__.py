"""
Template Plugin Client Interfaces

This module exports client interfaces for interacting with various template sources.
"""

from template_plugin.clients.base_client import BaseClient
from template_plugin.clients.backstage.client import BackstageClient
from template_plugin.clients.local.client import LocalClient

__all__ = [
    'BaseClient',
    'BackstageClient',
    'LocalClient',
]