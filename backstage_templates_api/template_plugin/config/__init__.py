"""
Configuration Module

This module exports configuration classes for the template plugin.
"""

from template_plugin.config.config import (
    BaseClientConfig,
    BackstageClientConfig,
    LocalClientConfig,
    ClientsConfig,
    load_config
)

__all__ = [
    'BaseClientConfig',
    'BackstageClientConfig',
    'LocalClientConfig',
    'ClientsConfig',
    'load_config'
] 