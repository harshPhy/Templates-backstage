"""
Template Client Interface

This module defines the abstract base class for all template clients.
Each client implementation must provide the functionality defined here.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from template_plugin.models.template_models import TemplateTaskResponse, TemplateParameterSchema, TemplateTask


class BaseClient(ABC):
    """
    Base abstract class that defines the interface for template clients.
    
    Any concrete implementation must implement all methods defined here.
    """
    
    @abstractmethod
    def list_templates(
        self,
        cloud_provider: Optional[str] = None,
        template_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        owner: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List available templates with optional filtering.
        
        Args:
            cloud_provider: Filter by cloud provider
            template_type: Filter by template type
            tags: Filter by tags
            owner: Filter by owner
            search: Search text across template metadata
            
        Returns:
            Dictionary with template items and total count
        """
        pass
    
    @abstractmethod
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """
        Get a specific template by its name.
        
        Args:
            template_name: The name of the template to retrieve
            
        Returns:
            Template data dictionary
        """
        pass
    
    @abstractmethod
    def get_template_parameters(self, template_name: str) -> Dict[str, Any]:
        """
        Get the parameter schema for a template.
        
        Args:
            template_name: The name of the template
            
        Returns:
            TemplateParameterSchema containing the parameter definitions
        """
        pass
    
    @abstractmethod
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
        Execute a template to create a component.
        
        Args:
            task: TemplateTask object with template name and parameters
            s3_bucket: S3 bucket containing the result (optional)
            s3_key: Key/path of the zip file in S3 (optional)
            local_path: Path where the file should be downloaded locally (optional)
            aws_access_key: AWS access key ID (optional)
            aws_secret_key: AWS secret access key (optional)
            aws_region: AWS region (default: us-east-1)
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            
        Returns:
            TemplateTaskResponse with task ID and status
        """
        pass
    
    @abstractmethod
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a template execution task.
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            TemplateTaskResponse with current status and outputs if available
        """
        pass