"""
Local Client Models

This module defines models specific to the local file-based client implementation.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import os
from datetime import datetime


class LocalTemplate(BaseModel):
    """Representation of a local template."""
    path: str
    yaml_data: Dict[str, Any]
    
    @property
    def name(self) -> str:
        """Get the template name."""
        return self.yaml_data.get("metadata", {}).get("name", "")
    
    @property
    def skeleton_dir(self) -> str:
        """Get the skeleton directory path."""
        return os.path.join(os.path.dirname(self.path), "skeleton")


class LocalTaskOutput(BaseModel):
    """Output from a local template task."""
    output_dir: str
    log_file: str = ""
    
    @property
    def exists(self) -> bool:
        """Check if the output directory exists."""
        return os.path.exists(self.output_dir)
    
    @property
    def creation_time(self) -> datetime:
        """Get the creation time of the output directory."""
        if self.exists:
            return datetime.fromtimestamp(os.path.getctime(self.output_dir))
        return datetime.now()


class LocalLogEntry(BaseModel):
    """Log entry for a local template task."""
    timestamp: datetime = Field(default_factory=datetime.now)
    level: str
    message: str
    details: Optional[Dict[str, Any]] = None 