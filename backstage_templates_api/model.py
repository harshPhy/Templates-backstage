from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    
class TemplateType(str, Enum):
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"
    WEBSITE = "website"
    LIBRARY = "library"
    OTHER = "other"
    SERVICE = "service"
    DOCUMENTATION = "documentation"


class TemplateTag(BaseModel):
    name: str
    description: Optional[str] = None


class TemplateMetadata(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    annotations: Optional[Dict[str, str]] = None
    cloud_provider: Optional[CloudProvider] = None


class TemplateSpec(BaseModel):
    owner: str
    type: TemplateType
    templater: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None


class TemplateOutput(BaseModel):
    links: Optional[List[Dict[str, str]]] = None


class Template(BaseModel):
    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: TemplateMetadata
    spec: TemplateSpec
    output: Optional[TemplateOutput] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True


class TemplateList(BaseModel):
    items: List[Template]
    total_count: int


class ErrorResponse(BaseModel):
    error: str
    status_code: int
    detail: Optional[str] = None


class TemplateParameter(BaseModel):
    """Template parameter value for creating a component."""
    name: str
    value: Any


class TemplateTask(BaseModel):
    """Request model for creating a component from a template."""
    template_name: str
    parameters: Dict[str, Any]
    dry_run: Optional[bool] = False


class TemplateTaskResponse(BaseModel):
    """Response model for a template task execution."""
    task_id: str
    template_name: str
    status: str
    created_at: str
    log_url: Optional[str] = None
    completion_url: Optional[str] = None
