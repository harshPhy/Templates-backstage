"""
Backstage Client Models

This module defines models specific to the Backstage client implementation.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime


class BackstageTemplate(BaseModel):
    """Representation of a template in Backstage."""
    metadata: Dict[str, Any]
    spec: Dict[str, Any] = {}
    kind: str = "Template"
    api_version: str = Field("scaffolder.backstage.io/v1beta3", alias="apiVersion")
    
    class Config:
        allow_population_by_field_name = True


class BackstageTaskResponse(BaseModel):
    """Response from Backstage task creation."""
    id: str
    spec: Dict[str, Any] = {}
    status: Optional[str] = None
    created_at: Optional[str] = None
    
    
class BackstageUser(BaseModel):
    """Representation of a Backstage user."""
    ref: str


class BackstageEntityRef(BaseModel):
    """Reference to a Backstage entity."""
    kind: str
    namespace: str
    name: str 