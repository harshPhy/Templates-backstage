"""
Configuration Classes

This module provides configuration classes for the template plugin.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
import os

class BaseClientConfig(BaseModel):
    """Base configuration for all clients"""
    DEFAULT_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    DEFAULT_HEADERS: Dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

class LocalClientConfig(BaseClientConfig):
    """Configuration specific to Local client"""
    templates_dir: str = "./templates"
    catalog_file: str = "./catalog-info.yaml"
    
    class Config:
        env_prefix = "LOCAL_"


class BackstageClientConfig(BaseClientConfig):
    """Configuration specific to Backstage client"""
    base_url: str = "http://localhost:7007/api"
    auth_token: Optional[str] = None
    
    # S3 download configuration
    s3_bucket: Optional[str] = os.getenv("BACKSTAGE_S3_BUCKET")
    local_path_template: Optional[str] = "/Users/harshithkoppula/Downloads/templates/{template_name}_{task_id}.zip"
    aws_access_key: Optional[str] = os.getenv("BACKSTAGE_AWS_ACCESS_KEY")
    aws_secret_key: Optional[str] = os.getenv("BACKSTAGE_AWS_SECRET_KEY")
    aws_region: str = os.getenv("BACKSTAGE_AWS_REGION")
    poll_interval: int = 5
    timeout: int = 300
    
    @property
    def auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        if self.auth_token:
            return {
                **self.DEFAULT_HEADERS,
                "Authorization": f"Bearer {self.auth_token}"
            }
        return self.DEFAULT_HEADERS
    
    class Config:
        env_prefix = "BACKSTAGE_"



class ClientsConfig(BaseModel):
    """Main configuration that includes all client configs"""
    backstage: BackstageClientConfig = Field(default_factory=BackstageClientConfig)
    local: LocalClientConfig = Field(default_factory=LocalClientConfig)
    
    # Global settings
    backstage_enabled: bool = True
    local_enabled: bool = True
    default_client: str = "backstage"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def load_config() -> ClientsConfig:
    """Load and return all configurations"""
    return ClientsConfig() 