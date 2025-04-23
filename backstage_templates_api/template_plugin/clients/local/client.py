"""
Local Template Client

This module provides the implementation of the TemplateClient interface for local file-based templates.
It reads templates from local files and provides template operations without relying on external services.
"""

import logging
import os
import uuid
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any
import boto3
import time
import re
import shutil

from template_plugin.clients.base_client import BaseClient
from template_plugin.models.template_models import TemplateTask, TemplateTaskResponse, TaskStatus
from template_plugin.utils.file_utils import read_yaml_file
from template_plugin.utils.template_utils import process_template_files
from template_plugin.errors.exceptions import (
    TemplateError,
    TemplateNotFoundError,
    TemplateExecutionError,
    FileAccessError
)
from template_plugin.config.config import LocalClientConfig
from template_plugin.s3 import S3Client

logger = logging.getLogger("local-template-client")

class LocalClient(BaseClient):
    """
    Implementation of BaseClient for local file-based templates.
    
    This client reads templates from local files and provides template operations
    without relying on external services.
    """
    
    def __init__(self, config: LocalClientConfig):
        """
        Initialize the Local template client.
        
        Args:
            config: Configuration for the client
        """
        self.config = config
        self.templates_dir = os.path.abspath(config.templates_dir)
        self.catalog_file = config.catalog_file
        if not os.path.exists(self.templates_dir):
            logger.warning(f"Templates directory does not exist: {self.templates_dir}")
            os.makedirs(self.templates_dir, exist_ok=True)
    
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
        try:
            logger.info(f"Listing templates from {self.templates_dir}")
            
            # If catalog file exists, use it to get template metadata
            if self.catalog_file and os.path.exists(self.catalog_file):
                templates = self._load_templates_from_catalog()
            else:
                # Otherwise, scan the templates directory
                templates = self._scan_templates_directory()
            
            # Apply filters
            filtered_templates = templates
            
            if cloud_provider:
                filtered_templates = [
                    t for t in filtered_templates 
                    if t.get("metadata", {}).get("cloud_provider") == cloud_provider
                ]
            
            if template_type:
                filtered_templates = [
                    t for t in filtered_templates 
                    if t.get("spec", {}).get("type") == template_type
                ]
            
            if tags:
                filtered_templates = [
                    t for t in filtered_templates 
                    if all(tag in t.get("metadata", {}).get("tags", []) for tag in tags)
                ]
            
            if owner:
                filtered_templates = [
                    t for t in filtered_templates 
                    if t.get("spec", {}).get("owner") == owner
                ]
            
            if search:
                search = search.lower()
                filtered_templates = [
                    t for t in filtered_templates 
                    if (search in t.get("metadata", {}).get("name", "").lower() or
                        search in t.get("metadata", {}).get("description", "").lower() or
                        search in t.get("metadata", {}).get("title", "").lower())
                ]
            
            return {
                "items": filtered_templates,
                "total_count": len(filtered_templates)
            }
        except Exception as e:
            logger.error(f"Failed to list templates: {str(e)}")
            raise TemplateError(f"Failed to list templates: {str(e)}")
    
    def _load_templates_from_catalog(self) -> List[Dict[str, Any]]:
        """
        Load templates from catalog file.
        
        Returns:
            List of templates
        """
        try:
            catalog_data = read_yaml_file(self.catalog_file)
            templates = []
            
            if catalog_data.get('kind') == 'Location' and 'spec' in catalog_data and 'targets' in catalog_data['spec']:
                template_paths = catalog_data['spec']['targets']
                logger.info(f"Found {len(template_paths)} template paths in catalog file")
                
                for path in template_paths:
                    if path.endswith('template.yaml'):
                        full_path = os.path.join(os.path.dirname(self.catalog_file), path)
                        try:
                            template = self._load_template_from_file(full_path)
                            templates.append(template)
                        except Exception as e:
                            logger.error(f"Error loading template {path}: {str(e)}")
            else:
                logger.warning(f"Catalog file doesn't have the expected structure")
                
            return templates
        except Exception as e:
            logger.error(f"Error loading catalog: {str(e)}")
            return []
    
    def _scan_templates_directory(self) -> List[Dict[str, Any]]:
        """
        Scan templates directory for template.yaml files.
        
        Returns:
            List of templates
        """
        templates = []
        
        for dirpath, dirnames, filenames in os.walk(self.templates_dir):
            if "template.yaml" in filenames:
                template_path = os.path.join(dirpath, "template.yaml")
                try:
                    template = self._load_template_from_file(template_path)
                    templates.append(template)
                except Exception as e:
                    logger.error(f"Error loading template {template_path}: {str(e)}")
        
        return templates
    
    def _load_template_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load a template from a file.
        
        Args:
            file_path: Path to the template file
            
        Returns:
            Template data
        """
        try:
            logger.info(f"Loading template from file: {file_path}")
            template_data = read_yaml_file(file_path)
            
            # Extract cloud provider from file path or tags
            cloud_provider = None
            if "/aws/" in file_path:
                cloud_provider = "aws"
            elif "/azure/" in file_path:
                cloud_provider = "azure"
            elif "/gcp/" in file_path:
                cloud_provider = "gcp"
                
            # Enhance metadata with cloud provider
            if 'metadata' in template_data:
                template_data['metadata']['cloud_provider'] = cloud_provider
                
            return template_data
        except Exception as e:
            logger.error(f"Failed to load template: {str(e)}")
            raise TemplateError(f"Failed to load template: {str(e)}")
    
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """
        Get a specific template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template details
        """
        try:
            logger.info(f"Finding template: {template_name}")
            
            # If catalog file exists, try to find the template there first
            if self.catalog_file and os.path.exists(self.catalog_file):
                templates = self._load_templates_from_catalog()
                for template in templates:
                    if template.get("metadata", {}).get("name") == template_name:
                        return template
            
            # Otherwise, try to find the template by scanning the directory
            for dirpath, dirnames, filenames in os.walk(self.templates_dir):
                if "template.yaml" in filenames:
                    template_path = os.path.join(dirpath, "template.yaml")
                    template = self._load_template_from_file(template_path)
                    if template.get("metadata", {}).get("name") == template_name:
                        return template
            
            # Template not found
            raise TemplateNotFoundError(f"Template not found: {template_name}")
        except TemplateNotFoundError:
            raise
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
            logger.info(f"Getting parameters for template: {template_name}")
            template = self.get_template(template_name)
            if template and template.get("spec", {}).get("parameters"):
                return {"parameters": template["spec"]["parameters"]}
            else:
                raise TemplateNotFoundError(f"Template parameters not found: {template_name}")
        except TemplateNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get template parameters: {str(e)}")
            raise TemplateError(f"Failed to get template parameters: {str(e)}")
    
    def execute_template(
        self, 
        task: TemplateTask,
        s3_bucket: Optional[str] = None,
        s3_key: Optional[str] = None,
        local_path: Optional[str] = None,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        aws_region: str = "us-east-1",
        poll_interval: int = 5,
        timeout: int = 300
    ) -> TemplateTaskResponse:
        """
        Execute a template to create a component with the provided parameters.
        
        For the local client, this processes the template files with the parameters
        but doesn't create actual resources. It's primarily for testing and preview.
        
        Args:
            task: Template task with parameters
            s3_bucket: S3 bucket containing the result (optional)
            s3_key: Key/path of the zip file in S3 (optional)
            local_path: Path where the file should be downloaded locally (optional)
            aws_access_key: AWS access key ID (optional)
            aws_secret_key: AWS secret access key (optional)
            aws_region: AWS region (default: us-east-1)
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            
        Returns:
            Task response
        """
        try:
            logger.info(f"Executing template: {task.template_name} (dry run: {task.dry_run})")
            
            # Get the template
            template = self.get_template(task.template_name)
            
            # Get the template directory
            template_dir = None
            for dirpath, dirnames, filenames in os.walk(self.templates_dir):
                if "template.yaml" in filenames:
                    temp_template_path = os.path.join(dirpath, "template.yaml")
                    temp_template = read_yaml_file(temp_template_path)
                    if temp_template.get("metadata", {}).get("name") == task.template_name:
                        template_dir = dirpath
                        break
            
            if not template_dir:
                raise TemplateNotFoundError(f"Template directory not found for: {task.template_name}")
            
            # Find skeleton directory
            skeleton_dir = os.path.join(template_dir, "skeleton")
            if not os.path.exists(skeleton_dir):
                raise FileAccessError(f"Skeleton directory not found: {skeleton_dir}")
            
            # Generate a task ID
            task_id = str(uuid.uuid4())
            
            # For local execution, create an output directory
            output_dir = os.path.join(self.templates_dir, f"output_{task_id}")
            os.makedirs(output_dir, exist_ok=True)
            
            if not task.dry_run:
                # Process template files with parameters - sync version
                process_template_files(
                    source_dir=skeleton_dir,
                    target_dir=output_dir,
                    values=task.parameters
                )
                status = TaskStatus.COMPLETED
            else:
                # For dry run, just validate parameters
                status = TaskStatus.PENDING
            
            # Construct response
            task_response = TemplateTaskResponse(
                task_id=task_id,
                template_name=task.template_name,
                status=status,
                created_at=datetime.now().isoformat(),
                log_url=f"file://{output_dir}/logs.txt",
                completion_url=f"file://{output_dir}"
            )
            
            # If S3 download parameters are provided
            if s3_bucket and s3_key and local_path:
                # For local client, we can immediately download from S3 if requested
                # since the template is already processed
                try:
                    logger.info(f"Downloading result from S3: s3://{s3_bucket}/{s3_key}")
                    
                    # Use our S3Client utility
                    s3_client = S3Client(
                        aws_access_key=aws_access_key,
                        aws_secret_key=aws_secret_key,
                        aws_region=aws_region
                    )
                    
                    # Download the file
                    download_success = s3_client.download_file(
                        bucket=s3_bucket,
                        key=s3_key,
                        local_path=local_path
                    )
                    
                    if download_success:
                        logger.info(f"Downloaded file to {local_path}")
                        # Update task response with download information
                        task_response.output_path = local_path
                    else:
                        logger.error("Failed to download file from S3")
                        task_response.error = "Failed to download file from S3"
                except Exception as e:
                    logger.error(f"Error downloading from S3: {str(e)}")
                    task_response.error = f"Error downloading from S3: {str(e)}"
            
            return task_response
        except Exception as e:
            logger.error(f"Failed to execute template: {str(e)}")
            raise TemplateExecutionError(f"Failed to execute template: {str(e)}")
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get status of a task.
        
        For the local client, this checks if the output directory exists.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task status
        """
        try:
            logger.info(f"Getting status for task: {task_id}")
            
            # Check if output directory exists
            output_dir = os.path.join(self.templates_dir, f"output_{task_id}")
            
            if os.path.exists(output_dir):
                # Check if log file has any errors
                log_file = os.path.join(output_dir, "logs.txt")
                status = "COMPLETED"
                
                if os.path.exists(log_file):
                    with open(log_file, "r") as f:
                        log_content = f.read()
                        if "ERROR" in log_content:
                            status = "FAILED"
                
                return {
                    "id": task_id,
                    "status": status,
                    "output_dir": output_dir,
                    "created_at": datetime.fromtimestamp(
                        os.path.getctime(output_dir)
                    ).isoformat()
                }
            else:
                raise TemplateNotFoundError(f"Task not found: {task_id}")
        except TemplateNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get task status: {str(e)}")
            raise TemplateError(f"Failed to get task status: {str(e)}") 