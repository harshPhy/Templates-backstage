"""
S3 Client Module

This module provides a client for interacting with AWS S3 service.
"""

import os
import logging
import boto3
import zipfile
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class S3Client:
    """
    S3 client wrapper for handling file operations with AWS S3.
    """
    
    def __init__(
        self,
        aws_access_key: Optional[str] = os.getenv("BACKSTAGE_AWS_ACCESS_KEY"),
        aws_secret_key: Optional[str] = os.getenv("BACKSTAGE_AWS_SECRET_KEY"),
        aws_region: str = os.getenv("BACKSTAGE_AWS_REGION", "us-east-1")
    ):
        """
        Initialize the S3 client.
        
        Args:
            aws_access_key: AWS access key ID
            aws_secret_key: AWS secret access key
            aws_region: AWS region
        """
        self.aws_region = aws_region
        
        # Initialize S3 client with credentials if provided
        if aws_access_key and aws_secret_key:
            self.client = boto3.client(
                "s3",
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
        else:
            # Use default credentials from environment or IAM role
            self.client = boto3.client("s3", region_name=aws_region)
            
        logger.debug(f"Initialized S3 client for region {aws_region}")
    
    def download_file(
        self,
        bucket: str,
        key: str,
        local_path: str
    ) -> bool:
        """
        Download a file from S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            local_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download the file
            self.client.download_file(Bucket=bucket, Key=key, Filename=local_path)
            logger.info(f"Downloaded file from s3://{bucket}/{key} to {local_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to download file from s3://{bucket}/{key}: {str(e)}")
            return False
    
    def upload_file(
        self,
        local_path: str,
        bucket: str,
        key: str,
        extra_args: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Upload a file to S3.
        
        Args:
            local_path: Local path of the file to upload
            bucket: S3 bucket name
            key: S3 object key
            extra_args: Extra arguments to pass to boto3 upload_file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Uploading to S3: {local_path} -> s3://{bucket}/{key}")
            self.client.upload_file(local_path, bucket, key, ExtraArgs=extra_args)
            logger.info(f"Successfully uploaded file to s3://{bucket}/{key}")
            return True
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            return False
    
    def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        expiration: int = 3600
    ) -> Optional[str]:
        """
        Generate a presigned URL for an S3 object.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            expiration: URL expiration time in seconds
            
        Returns:
            Presigned URL or None if error
        """
        try:
            logger.info(f"Generating presigned URL for s3://{bucket}/{key}")
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return None
            
    def unzip_file(self, local_zip_path, extract_dir):
        """
        Unzip a local file and optionally delete the zip file.
        
        Args:
            local_zip_path: Path to the zip file
            extract_dir: Directory to extract to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create extraction directory if it doesn't exist
            os.makedirs(extract_dir, exist_ok=True)
            
            # Extract the zip file
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            logger.info(f"Extracted {local_zip_path} to {extract_dir}")
            
            # Delete the original zip file
            os.remove(local_zip_path)
            logger.info(f"Deleted zip file {local_zip_path}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to unzip file {local_zip_path}: {str(e)}")
            return False 