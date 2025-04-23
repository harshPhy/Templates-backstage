"""
Client Models

This module provides common models used across different client implementations.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime


class ClientResponse(BaseModel):
    """Base class for all client responses."""
    pass


class TemplateList(BaseModel):
    """Model representing a list of templates."""
    items: List[Dict[str, Any]]
    total_count: int


class TemplateDetails(BaseModel):
    """Model representing template details."""
    name: str
    title: str
    description: Optional[str] = None
    metadata: Dict[str, Any]
    spec: Dict[str, Any]
    parameters: Optional[List[Dict[str, Any]]] = None


class TaskStatus(BaseModel):
    """Model representing the status of a template execution task."""
    task_id: str
    status: str
    created_at: str
    updated_at: Optional[str] = None
    details: Optional[Dict[str, Any]] = None 