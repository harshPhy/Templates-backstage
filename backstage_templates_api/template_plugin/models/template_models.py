"""
Template Models

This module defines data structures for template tasks and responses.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task execution status values"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TemplateParameter(BaseModel):
    """
    Model representing a parameter required by a template.
    """
    name: str = Field(..., description="Name of the parameter")
    title: Optional[str] = Field(default=None, description="Human-readable title")
    description: Optional[str] = Field(default=None, description="Parameter description")
    type: str = Field(..., description="Data type of the parameter")
    required: bool = Field(default=True, description="Whether the parameter is required")
    default: Optional[Any] = Field(default=None, description="Default value if not provided")
    enum: Optional[List[Any]] = Field(default=None, description="List of allowed values for the parameter")


class TemplateTask(BaseModel):
    """
    Model representing a template execution task.
    """
    template_name: str = Field(..., description="Name of the template to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters for template execution")
    dry_run: bool = Field(default=False, description="Whether to perform a dry run without actual creation")
    owner: Optional[str] = Field(default=None, description="Owner of the created component")
    description: Optional[str] = Field(default=None, description="Description of the created component")


class TemplateTaskResponse(BaseModel):
    """
    Response model for template task creation.
    """
    task_id: str = Field(..., description="Unique identifier for the task")
    template_name: str = Field(..., description="Name of the template that was executed")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status of the task")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Task creation timestamp")
    log_url: Optional[str] = Field(default=None, description="URL to view task logs")
    completion_url: Optional[str] = Field(default=None, description="URL to view task completion")
    output_path: Optional[str] = Field(default=None, description="Path to the task output when completed")
    error: Optional[str] = Field(default=None, description="Error message if task failed")


class TemplateLog(BaseModel):
    """
    Represents a log entry for a template execution task.
    """
    task_id: str = Field(..., description="ID of the task")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO formatted timestamp of the log entry"
    )
    level: str = Field(..., description="Log level (INFO, ERROR, etc.)")
    message: str = Field(..., description="Log message")
    step_id: Optional[str] = Field(None, description="ID of the step that generated the log")
    step_name: Optional[str] = Field(None, description="Name of the step that generated the log")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


class Template(BaseModel):
    """
    Represents a template definition.
    
    This is a simplified model used to represent templates across different sources.
    """
    api_version: str = Field(..., description="API version of the template")
    kind: str = Field(..., description="Kind of the template (Template)")
    metadata: Dict[str, Any] = Field(..., description="Template metadata")
    spec: Dict[str, Any] = Field(..., description="Template specification")
    output: Optional[Dict[str, Any]] = Field(None, description="Template output definition")


class TemplateList(BaseModel):
    """
    Represents a list of templates.
    """
    items: List[Template] = Field(..., description="List of templates")
    total_count: int = Field(..., description="Total number of templates")


class TemplateParameterSchema(BaseModel):
    """
    Model representing the schema of parameters for a template.
    """
    parameters: List[TemplateParameter] = Field(default_factory=list, description="List of parameters")
