"""
AWS Utilities (Backward Compatibility Module)

This module provides backward compatibility with the previous aws_utils location.
It imports from the new S3 module and re-exports the same functionality.
"""

import os
from typing import Optional
from template_plugin.s3 import S3Client

def get_s3_client(
    aws_access_key: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
) -> S3Client:
    """
    Factory function to get an S3 client instance.
    
    Args:
        aws_access_key: AWS access key ID
        aws_secret_key: AWS secret access key
        aws_region: AWS region
        
    Returns:
        S3Client instance
    """
    return S3Client(aws_access_key, aws_secret_key, aws_region)

# Re-export S3Client
__all__ = ['S3Client', 'get_s3_client'] 