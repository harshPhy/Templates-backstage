"""
Template Plugin - Main orchestration class

This module provides the main TemplatePlugin class that orchestrates template operations,
selecting the appropriate client implementation based on configuration.
"""

import logging
from typing import Dict, List, Optional, Any, Union
import boto3
import os
import time

from template_plugin.clients.base_client import BaseClient
from template_plugin.clients.backstage import BackstageClient
from template_plugin.clients.local import LocalClient
from template_plugin.models.template_models import TemplateTask, TemplateTaskResponse, TaskStatus
from template_plugin.models.config_models import TemplatePluginConfig
from template_plugin.errors.exceptions import TemplateError, ClientInitializationError
from template_plugin.config.config import ClientsConfig, load_config

logger = logging.getLogger("template-plugin")

class TemplatePlugin:
    """
    Main orchestration class for the Template Plugin.
    
    This class selects and manages the appropriate template client based on configuration.
    It provides a unified interface for all template operations.
    """
    
    def __init__(self, config: Optional[Union[TemplatePluginConfig, ClientsConfig]] = None):
        """
        Initialize the Template Plugin with configuration.
        
        Args:
            config: Configuration for the template plugin, or None to use default
        """
        # If no config provided, load default config
        if config is None:
            self.config = load_config()
        # If old-style config provided, convert to new style
        elif isinstance(config, TemplatePluginConfig):
            # For backwards compatibility
            self.config = ClientsConfig(
                backstage_enabled=config.backstage_enabled,
                local_enabled=config.local_enabled,
                default_client=config.default_client,
                backstage={
                    "base_url": config.backstage.base_url,
                    "auth_token": config.backstage.auth_token
                },
                local={
                    "templates_dir": config.local.templates_dir,
                    "catalog_file": config.local.catalog_file
                }
            )
        else:
            self.config = config
        
        self.clients: Dict[str, BaseClient] = {}
        self._initialize_clients()
        
    def _initialize_clients(self) -> None:
        """Initialize template clients based on configuration."""
        try:
            # Initialize Backstage client if configured
            if self.config.backstage_enabled:
                logger.info("Initializing Backstage template client")
                self.clients["backstage"] = BackstageClient(self.config.backstage)
            
            # Initialize Local client if configured
            if self.config.local_enabled:
                logger.info("Initializing Local template client")
                self.clients["local"] = LocalClient(self.config.local)
                
            # Set default client
            self.default_client = self.config.default_client
            if self.default_client not in self.clients:
                available_clients = list(self.clients.keys())
                if available_clients:
                    self.default_client = available_clients[0]
                    logger.warning(
                        f"Default client '{self.config.default_client}' not available. "
                        f"Using '{self.default_client}' instead."
                    )
                else:
                    raise ClientInitializationError("No template clients were initialized")
                    
        except Exception as e:
            logger.error(f"Failed to initialize template clients: {str(e)}")
            raise ClientInitializationError(f"Failed to initialize template clients: {str(e)}")
    
    def get_client(self, client_name: Optional[str] = None) -> BaseClient:
        """
        Get a template client by name, or the default client if no name is specified.
        
        Args:
            client_name: Name of the client to get, or None for default
            
        Returns:
            The requested template client
            
        Raises:
            ClientInitializationError: If the requested client is not available
        """
        client_name = client_name or self.default_client
        
        if client_name not in self.clients:
            raise ClientInitializationError(
                f"Template client '{client_name}' not available. "
                f"Available clients: {list(self.clients.keys())}"
            )
            
        return self.clients[client_name]
    
    def list_templates(
        self,
        cloud_provider: Optional[str] = None,
        template_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owner: Optional[str] = None,
        search: Optional[str] = None,
        client_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List templates with optional filtering.
        
        Args:
            cloud_provider: Filter by cloud provider
            template_type: Filter by template type
            tags: Filter by tags
            owner: Filter by owner
            search: Search in name and description
            client_name: Name of the client to use, or None for default
            
        Returns:
            List of templates
        """
        client = self.get_client(client_name)
        return client.list_templates(
            cloud_provider=cloud_provider,
            template_type=template_type,
            tags=tags,
            owner=owner,
            search=search
        )
    
    def get_template(
        self,
        template_name: str,
        client_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a specific template by name.
        
        Args:
            template_name: Name of the template
            client_name: Name of the client to use, or None for default
            
        Returns:
            Template details
        """
        client = self.get_client(client_name)
        return client.get_template(template_name)
    
    def get_template_parameters(
        self,
        template_name: str,
        client_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get parameter schema for a specific template.
        
        Args:
            template_name: Name of the template
            client_name: Name of the client to use, or None for default
            
        Returns:
            Template parameter schema
        """
        client = self.get_client(client_name)
        return client.get_template_parameters(template_name)
    
    def execute_template(
        self,
        template_name: str,
        parameters: Dict[str, Any],
        dry_run: bool = False,
        client_name: Optional[str] = None,
        s3_bucket: Optional[str] = None,
        s3_key: Optional[str] = None,
        local_path: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        aws_region: Optional[str] = None,
        poll_interval: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> TemplateTaskResponse:
        """
        Execute a template to create a component with the provided parameters.
        
        If S3 download parameters are provided, also wait for task completion
        and download the result from S3. If s3_key is not provided, it will be
        auto-determined from the task output or generated from template name and task ID.
        
        Args:
            template_name: Name of the template
            parameters: Template parameters
            dry_run: Whether to perform a dry run
            client_name: Name of the client to use, or None for default
            s3_bucket: S3 bucket containing the result (optional, overrides client config)
            s3_key: Key/path of the zip file in S3 (optional, auto-determined if not provided)
            local_path: Path where the file should be downloaded locally (optional)
            aws_access_key: AWS access key ID (optional, overrides client config)
            aws_secret_key: AWS secret access key (optional, overrides client config)
            aws_region: AWS region (optional, overrides client config)
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            
        Returns:
            Task response with download information if S3 download was performed
        """
        client = self.get_client(client_name)
        task = TemplateTask(
            template_name=template_name,
            parameters=parameters,
            dry_run=dry_run
        )
        
        # Pass S3 download parameters to client
        return client.execute_template(
            task=task,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            local_path=local_path,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_region=aws_region,
            poll_interval=poll_interval,
            timeout=timeout
        )
    
    def get_task_status(
        self,
        task_id: str,
        client_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get status of a task.
        
        Args:
            task_id: ID of the task
            client_name: Name of the client to use, or None for default
            
        Returns:
            Task status
        """
        client = self.get_client(client_name)
        return client.get_task_status(task_id)