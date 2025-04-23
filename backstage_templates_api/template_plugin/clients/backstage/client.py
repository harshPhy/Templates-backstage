"""
Backstage Template Client

This module provides the implementation of the BaseClient interface for Backstage.
It communicates with the Backstage API to perform template operations.
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import os
import time
import boto3

import httpx

from template_plugin.models.template_models import TaskStatus            
from template_plugin.clients.base_client import BaseClient
from template_plugin.models.template_models import TemplateTask, TemplateTaskResponse
from template_plugin.clients.backstage.models import BackstageTemplate, BackstageTaskResponse
from template_plugin.errors.exceptions import (
    TemplateError,
    TemplateNotFoundError,
    TemplateExecutionError,
    ConnectionError
)
from template_plugin.config.config import BackstageClientConfig
from template_plugin.s3 import S3Client, S3Downloader

logger = logging.getLogger("backstage-template-client")

class BackstageClient(BaseClient):
    """
    Implementation of BaseClient for Backstage.
    
    This client communicates with the Backstage API to perform template operations.
    """
    
    def __init__(self, config: BackstageClientConfig):
        """
        Initialize the Backstage template client.
        
        Args:
            config: Configuration for the client
        """
        self.config = config
        self.base_url = config.base_url.rstrip("/")
        self.auth_token = config.auth_token
        
        # S3 config with default values
        self.s3_config = {
            "bucket": getattr(config, "s3_bucket", None),
            "local_path_template": getattr(config, "local_path_template", "/Users/harshithkoppula/Downloads/templates/{template_name}_{task_id}.zip"),
            "aws_access_key": getattr(config, "aws_access_key", None),
            "aws_secret_key": getattr(config, "aws_secret_key", None),
            "aws_region": getattr(config, "aws_region", "us-east-1"),
            "poll_interval": getattr(config, "poll_interval", 5),
            "timeout": getattr(config, "timeout", 300)
        }
        
        # Pre-compute the UI base URL
        self.ui_base_url = self.base_url.replace("/api", "")
        
    def _get_client(self) -> httpx.Client:
        """
        Get an HTTP client for communicating with the Backstage API.
        
        Returns:
            An HTTP client with the appropriate headers
        """
        return httpx.Client(
            base_url=self.base_url,
            headers=self.config.auth_headers,
            timeout=self.config.DEFAULT_TIMEOUT
        )
    
    def _request(
        self, 
        method: str, 
        path: str, 
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the Backstage API.
        
        Args:
            method: HTTP method
            path: API path
            params: Query parameters
            json_data: JSON request body
            
        Returns:
            Response data
            
        Raises:
            ConnectionError: If there is a connection error
            TemplateError: If there is an API error
        """
        url = f"{path}"
        logger.debug(f"Making {method} request to {url}")
        
        try:
            with self._get_client() as client:
                response = client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data
                )
                
                if response.status_code == 404:
                    raise TemplateNotFoundError(f"Resource not found: {url}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise TemplateError(f"Backstage API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise ConnectionError(f"Connection error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise TemplateError(f"Unexpected error: {str(e)}")
    
    def list_templates(
        self,
        cloud_provider: Optional[str] = None,
        template_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owner: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List templates with optional filtering.
        
        Args:
            cloud_provider: Filter by cloud provider
            template_type: Filter by template type
            tags: Filter by tags
            owner: Filter by owner
            search: Search in name and description
            
        Returns:
            List of templates
        """
        params = {}
        if cloud_provider:
            params["cloud_provider"] = cloud_provider
        if template_type:
            params["template_type"] = template_type
        if tags:
            params["tag"] = tags
        if owner:
            params["owner"] = owner
        if search:
            params["search"] = search
            
        try:
            # Fetch templates from Backstage Catalog API
            logger.info(f"Fetching templates with filters: {params}")
            response = self._request(
                method="GET",
                path="/catalog/entities",
                params={"filter": "kind=Template", **params}
            )
            
            # Map Backstage response to TemplateList format
            templates = []
            for item in response:
                template = self._map_backstage_template(item)
                templates.append(template)
                
            return {
                "items": templates,
                "total_count": len(templates)
            }
        except Exception as e:
            logger.error(f"Failed to list templates: {str(e)}")
            raise TemplateError(f"Failed to list templates: {str(e)}")
            
    def _map_backstage_template(self, backstage_template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a Backstage template to our template format.
        
        Args:
            backstage_template: Template from Backstage API
            
        Returns:
            Mapped template
        """
        metadata = backstage_template.get("metadata", {})
        spec = backstage_template.get("spec", {})
        
        # Determine cloud provider from tags
        cloud_provider = None
        tags = metadata.get("tags", [])
        if "aws" in tags:
            cloud_provider = "aws"
        elif "azure" in tags:
            cloud_provider = "azure"
        elif "gcp" in tags:
            cloud_provider = "gcp"
            
        return {
            "apiVersion": backstage_template.get("apiVersion", "scaffolder.backstage.io/v1beta3"),
            "kind": backstage_template.get("kind", "Template"),
            "metadata": {
                "name": metadata.get("name", ""),
                "title": spec.get("title", ""),
                "description": metadata.get("description", ""),
                "tags": metadata.get("tags", []),
                "annotations": metadata.get("annotations", {}),
                "cloud_provider": cloud_provider
            },
            "spec": {
                "owner": spec.get("owner", ""),
                "type": spec.get("type", "other"),
                "templater": spec.get("templater", "v1beta3"),
                "parameters": spec.get("parameters", [])
            },
            "output": {
                "links": spec.get("output", {}).get("links", [])
            }
        }
    
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """
        Get a specific template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template details
        """
        try:
            logger.info(f"Fetching template: {template_name}")
            response = self._request(
                method="GET",
                path=f"/catalog/entities/by-name/template/default/{template_name}"
            )
            return self._map_backstage_template(response)
        except TemplateNotFoundError:
            raise TemplateNotFoundError(f"Template not found: {template_name}")
        except Exception as e:
            logger.error(f"Failed to get template: {str(e)}")
            raise TemplateError(f"Failed to get template: {str(e)}")
    
    def get_template_parameters(self, template_name: str) -> Dict[str, Any]:
        """
        Get parameter schema for a specific template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template parameter schema
        """
        try:
            # First try to get the template to extract parameters directly
            template = self.get_template(template_name)
            if template and template.get("spec", {}).get("parameters"):
                logger.info(f"Using parameters from template metadata for: {template_name}")
                return {"parameters": template["spec"]["parameters"]}
                
            # If no parameters in template metadata, try the parameter schema endpoint
            # The expected format is /api/scaffolder/v2/templates/:namespace/:kind/:name
            # Default namespace and kind if not specified in the template name
            namespace = "default"
            kind = "template"
            name = template_name
            
            # Check if template_name includes namespace and kind (format: namespace:kind:name)
            if ":" in template_name:
                parts = template_name.split(":")
                if len(parts) == 3:
                    namespace, kind, name = parts
                elif len(parts) == 2:
                    namespace, name = parts
            
            logger.info(f"Fetching parameter schema for template: {namespace}/{kind}/{name}")
            
            response = self._request(
                method="GET",
                path=f"/scaffolder/v2/templates/{namespace}/{kind}/{name}"
            )
            
            # Extract parameter schema from the response
            if "parameters" in response:
                return {"parameters": response["parameters"]}
            return response
            
        except TemplateNotFoundError:
            raise TemplateNotFoundError(f"Template parameters not found: {template_name}")
        except Exception as e:
            logger.error(f"Failed to get template parameters: {str(e)}")
            raise TemplateError(f"Failed to get template parameters: {str(e)}")
    
    def _get_s3_params(
        self,
        s3_bucket: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        aws_region: Optional[str] = None,
        poll_interval: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get S3 parameters with fallbacks to configured defaults.
        
        Args:
            s3_bucket: S3 bucket name (optional)
            aws_access_key: AWS access key ID (optional)
            aws_secret_key: AWS secret access key (optional)
            aws_region: AWS region (optional)
            poll_interval: Poll interval in seconds (optional)
            timeout: Timeout in seconds (optional)
            
        Returns:
            Dictionary of S3 parameters with defaults applied
        """
        return {
            "s3_bucket": s3_bucket or self.s3_config.get("bucket"),
            "aws_access_key": aws_access_key or self.s3_config.get("aws_access_key"),
            "aws_secret_key": aws_secret_key or self.s3_config.get("aws_secret_key"),
            "aws_region": aws_region or self.s3_config.get("aws_region"),
            "poll_interval": poll_interval or self.s3_config.get("poll_interval"),
            "timeout": timeout or self.s3_config.get("timeout")
        }

    def _initialize_s3_downloader(
        self,
        task_id: str,
        task: TemplateTask,
        s3_bucket: Optional[str] = None,
        s3_key: Optional[str] = None,
        local_path: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        aws_region: Optional[str] = None,
        poll_interval: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> Tuple[bool, Optional[S3Downloader], Optional[str], Optional[str]]:
        """
        Initialize the S3 downloader with appropriate configuration.
        
        Args:
            task_id: ID of the template execution task
            task: Template task with parameters
            s3_bucket: S3 bucket containing the result 
            s3_key: Key/path of the zip file in S3
            local_path: Path where the file should be downloaded locally
            aws_access_key: AWS access key ID
            aws_secret_key: AWS secret access key
            aws_region: AWS region
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            
        Returns:
            Tuple containing:
            - Success flag (bool)
            - S3Downloader instance (or None if initialization failed)
            - Configured local path (or None if not applicable)
            - Error message (or None if successful)
        """
        try:
            # Get S3 parameters with defaults
            s3_params = self._get_s3_params(s3_bucket=s3_bucket,aws_access_key=aws_access_key,aws_secret_key=aws_secret_key,aws_region=aws_region,poll_interval=poll_interval,timeout=timeout)
            
            # If local_path wasn't provided, generate one from template
            if not local_path and self.s3_config.get("local_path_template"):
                local_path = self.s3_config.get("local_path_template").format(template_name=task.template_name,task_id=task_id)
            
            # If bucket is configured, set up downloader
            if s3_params["s3_bucket"] and local_path:
                # Create S3 client
                s3_client = S3Client(aws_access_key=s3_params["aws_access_key"], aws_secret_key=s3_params["aws_secret_key"], aws_region=s3_params["aws_region"])
                
                # Create downloader
                s3_downloader = S3Downloader(
                    s3_client=s3_client,
                    task_id=task_id,
                    task=task,
                    s3_bucket=s3_params["s3_bucket"],
                    s3_key=s3_key,
                    local_path=local_path,
                    poll_interval=s3_params["poll_interval"],
                    timeout=s3_params["timeout"],
                    task_status_callback=self.get_task_status
                )
                
                return True, s3_downloader, local_path, None
            
            return False, None, local_path, "S3 bucket or local path not configured"
            
        except Exception as e:
            logger.error(f"Failed to initialize S3 downloader: {str(e)}")
            return False, None, None, f"Failed to initialize S3 downloader: {str(e)}"
    
    def _get_task_urls(self, task_id: str) -> Tuple[str, str]:
        """
        Generate log and completion URLs for a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Tuple of (log_url, completion_url)
        """
        log_url = f"{self.ui_base_url}/create/tasks/{task_id}/logs"
        completion_url = f"{self.ui_base_url}/create/tasks/{task_id}/completion"
        return log_url, completion_url
    
    def execute_template(
        self, 
        task: TemplateTask,
        s3_bucket: Optional[str] = os.getenv("BACKSTAGE_S3_BUCKET"),
        s3_key: Optional[str] = None,
        local_path: Optional[str] = None,
        aws_access_key: Optional[str] = os.getenv("BACKSTAGE_AWS_ACCESS_KEY"),
        aws_secret_key: Optional[str] = os.getenv("BACKSTAGE_AWS_SECRET_KEY"),
        aws_region: str = os.getenv("BACKSTAGE_AWS_REGION"),
        poll_interval: int = 5,
        timeout: int = 300
    ) -> TemplateTaskResponse:
        """
        Execute a template to create a component with the provided parameters.
        
        Args:
            task: Template task with parameters
            s3_bucket: S3 bucket containing the result (optional, overrides config)
            s3_key: Key/path of the zip file in S3 (optional)
            local_path: Path where the file should be downloaded locally (optional)
            aws_access_key: AWS access key ID (optional, overrides config)
            aws_secret_key: AWS secret access key (optional, overrides config)
            aws_region: AWS region (default: us-east-1, overrides config)
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            
        Returns:
            Task response
        """
        try:
            logger.info(f"Executing template: {task.template_name}")
            
            # Prepare payload for Backstage
            payload = {
                "templateRef": f"template:default/{task.template_name}",
                "values": task.parameters,
                "secrets": {},
                "isDryRun": task.dry_run
            }
            
            response = self._request(
                method="POST",
                path="/scaffolder/v2/tasks",
                json_data=payload
            )
            
            # Get task_id from response
            task_id = response.get("id", str(uuid.uuid4()))
            
            # Get log and completion URLs
            log_url, completion_url = self._get_task_urls(task_id)
                      
            task_response = TemplateTaskResponse(
                task_id=task_id,
                template_name=task.template_name,
                status=TaskStatus.PENDING,
                created_at=datetime.now().isoformat(),
                log_url=log_url,
                completion_url=completion_url
            )
            
            # Initialize S3 downloader if needed
            init_success, s3_downloader, configured_local_path, error = self._initialize_s3_downloader(
                task_id=task_id,
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
            
            # If initialization was successful, download and extract
            if init_success and s3_downloader:
                try:
                    success, output_path, error = s3_downloader.download_and_extract()
                    
                    if success and output_path:
                        task_response.output_path = output_path
                        task_response.status = TaskStatus.COMPLETED
                    else:
                        task_response.error = error or "Unknown error during download"
                except Exception as e:
                    logger.error(f"Error during S3 download: {str(e)}")
                    task_response.error = f"Error during S3 download: {str(e)}"
                    # Continue with the original task response even if download fails
            elif error:
                logger.warning(f"S3 downloader initialization failed: {error}")
                # Only set error if it's not already set
                if not task_response.error:
                    task_response.error = error
            
            return {
                "task_id": task_response.task_id,
                "template_name": task_response.template_name,
                "status": task_response.status,
                "created_at": task_response.created_at,
                "log_url": task_response.log_url,
                "completion_url": task_response.completion_url,
                "output_path": task_response.output_path,
                "error": task_response.error
            }
        except Exception as e:
            logger.error(f"Failed to execute template: {str(e)}")
            raise TemplateExecutionError(f"Failed to execute template: {str(e)}")
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get status of a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task status
        """
        try:
            logger.info(f"Fetching task status: {task_id}")
            return self._request(
                method="GET",
                path=f"/scaffolder/v2/tasks/{task_id}"
            )
        except TemplateNotFoundError:
            raise TemplateNotFoundError(f"Task not found: {task_id}")
        except Exception as e:
            logger.error(f"Failed to get task status: {str(e)}")
            raise TemplateError(f"Failed to get task status: {str(e)}") 