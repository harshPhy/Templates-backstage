"""
Configuration models for template clients.

This module provides Pydantic models for client configuration.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class BaseClientConfig(BaseModel):
    """Base configuration for all clients."""
    pass


class BackstageConfig(BaseClientConfig):
    """Configuration for Backstage client."""
    base_url: str = Field(default="http://localhost:7007/api", description="Base URL of the Backstage API")
    auth_token: Optional[str] = Field(None, description="Authentication token")


class LocalConfig(BaseClientConfig):
    """Configuration for Local client."""
    templates_dir: str = Field(..., description="Directory containing templates")
    catalog_file: Optional[str] = Field(None, description="Optional catalog file")


class CustomConfig(BaseModel):
    """
    Configuration for custom template clients.
    
    This is a generic configuration that can be extended for custom clients.
    """
    settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom settings for the client"
    )


class TemplatePluginConfig(BaseModel):
    """Configuration for the Template Plugin."""
    backstage_enabled: bool = Field(True, description="Whether Backstage client is enabled")
    backstage_api_url: Optional[str] = Field(None, description="Backstage API URL")
    backstage_auth_token: Optional[str] = Field(None, description="Backstage auth token")
    local_enabled: bool = Field(True, description="Whether Local client is enabled")
    templates_dir: Optional[str] = Field(None, description="Templates directory")
    catalog_file: Optional[str] = Field(None, description="Catalog file path")
    default_client: str = Field("backstage", description="Default client type")
    
    # Client-specific settings
    backstage: BackstageConfig = Field(
        default_factory=lambda: BackstageConfig(),
        description="Backstage client configuration"
    )
    local: LocalConfig = Field(
        default_factory=lambda: LocalConfig(templates_dir="./templates"),
        description="Local client configuration"
    )
    custom: Dict[str, CustomConfig] = Field(
        default_factory=dict,
        description="Custom client configurations"
    )
    
    @validator('default_client')
    def validate_default_client(cls, v, values):
        """Validate that the default client is enabled."""
        if v == 'backstage' and not values.get('backstage_enabled', True):
            raise ValueError("Default client 'backstage' is not enabled")
        if v == 'local' and not values.get('local_enabled', True):
            raise ValueError("Default client 'local' is not enabled")
        if v not in ['backstage', 'local'] and not values.get('custom_enabled', False):
            raise ValueError(f"Default client '{v}' is not a standard client and custom clients are not enabled")
        return v
