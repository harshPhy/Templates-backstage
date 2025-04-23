"""
Client Factory

This module provides a factory for creating template clients based on configuration.
"""

import importlib
import logging
from typing import Dict, Type, Optional, Any

from template_plugin.clients.base_client import BaseClient
from template_plugin.models.config_models import BaseClientConfig, BackstageConfig, LocalConfig
from template_plugin.errors.exceptions import ClientInitializationError
from template_plugin.config.config import (
    ClientsConfig, 
    BackstageClientConfig, 
    LocalClientConfig,
    load_config
)

logger = logging.getLogger("client-factory")

class ClientFactory:
    """Factory for creating template clients."""
    
    # Map of client types to module paths
    _client_modules: Dict[str, str] = {
        "backstage": "template_plugin.clients.backstage",
        "local": "template_plugin.clients.local"
    }
    
    # Map of client types to config types
    _config_types: Dict[str, Type] = {
        "backstage": BackstageClientConfig,
        "local": LocalClientConfig
    }
    
    # Map of client types to class names
    _client_classes: Dict[str, str] = {
        "backstage": "BackstageClient",
        "local": "LocalClient"
    }
    
    @classmethod
    def create_client(cls, client_type: str, custom_config: Optional[Dict[str, Any]] = None) -> BaseClient:
        """
        Create a template client of the specified type.
        
        Args:
            client_type: Type of client to create ("backstage" or "local")
            custom_config: Optional custom configuration for the client
            
        Returns:
            An instance of the requested template client
            
        Raises:
            ClientInitializationError: If the client type is unknown or initialization fails
        """
        # Check if client type is supported
        if client_type not in cls._client_modules:
            raise ClientInitializationError(f"Unknown client type: {client_type}")
        
        try:
            # Load base configuration
            base_config = load_config()
            
            # Get config class for this client type
            config_class = cls._config_types[client_type]
            
            # Prepare config: start with base config, override with custom config
            if client_type == "backstage":
                config = base_config.backstage
                if custom_config:
                    # Override with any custom config values
                    if "auth_token" in custom_config:
                        config.auth_token = custom_config.get("auth_token")
                    if "base_url" in custom_config:
                        config.base_url = custom_config.get("base_url")
            elif client_type == "local":
                config = base_config.local
                if custom_config:
                    # Override with any custom config values
                    if "templates_dir" in custom_config:
                        config.templates_dir = custom_config.get("templates_dir")
                    if "catalog_file" in custom_config:
                        config.catalog_file = custom_config.get("catalog_file")
            
            # Import client module
            module_path = cls._client_modules[client_type]
            logger.info(f"Importing client module: {module_path}")
            module = importlib.import_module(module_path)
            
            # Get client class
            client_class_name = cls._client_classes[client_type]
            client_class = getattr(module, client_class_name)
            
            # Create client instance with config
            logger.info(f"Creating client instance: {client_class_name}")
            return client_class(config)
            
        except ImportError as e:
            logger.error(f"Failed to import client module: {str(e)}")
            raise ClientInitializationError(f"Failed to import client module: {str(e)}")
        except AttributeError as e:
            logger.error(f"Client class not found: {str(e)}")
            raise ClientInitializationError(f"Client class not found: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to initialize client: {str(e)}")
            raise ClientInitializationError(f"Failed to initialize client: {str(e)}")

# bkstage_client = ClientFactory.create_client("backstage", {})
# bkstage_client.get_template_list()