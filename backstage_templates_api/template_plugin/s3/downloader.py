"""
S3 Downloader Module

This module provides functionality for downloading and extracting files from S3.
"""

import os
import logging
import time
from typing import Optional, Dict, Any, Tuple, Callable

from template_plugin.s3.client import S3Client
from template_plugin.models.template_models import TemplateTask, TaskStatus

logger = logging.getLogger(__name__)

class S3Downloader:
    """
    Handles downloading and extracting template results from S3.
    """
    
    def __init__(
        self, 
        s3_client: S3Client,
        task_id: str,
        task: TemplateTask,
        s3_bucket: str,
        s3_key: Optional[str] = None,
        local_path: Optional[str] = None,
        poll_interval: int = 5,
        timeout: int = 300,
        task_status_callback: Optional[Callable] = None
    ):
        """
        Initialize the downloader.
        
        Args:
            s3_client: S3 client instance
            task_id: The task ID
            task: Template task with parameters
            s3_bucket: S3 bucket containing the result
            s3_key: Key/path of the zip file in S3 (optional)
            local_path: Path where the file should be downloaded locally (optional)
            poll_interval: How often to check task status (seconds)
            timeout: Maximum time to wait for completion (seconds)
            task_status_callback: Function to call to get task status
        """
        self.s3_client = s3_client
        self.task_id = task_id
        self.task = task
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.local_path = local_path
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.task_status_callback = task_status_callback
    
    def determine_s3_key(self, task_status_data: Dict[str, Any]) -> Optional[str]:
        """
        Determine the S3 key to use for downloading.
        
        Args:
            task_status_data: Task status data
            
        Returns:
            S3 key or None if not found
        """
        # If s3_key is already set, use it
        if self.s3_key:
            return self.s3_key
            
        # Try to determine from task parameters
        if 'name' in self.task.parameters:
            return f"templates/{self.task.parameters['name']}.zip"
            
        # Try to extract s3_key from task output if available
        if ("output" in task_status_data and 
            "steps" in task_status_data.get("output", {}) and
            isinstance(task_status_data["output"]["steps"], list)):
            
            # Look for the create-zip step output
            for step in task_status_data["output"]["steps"]:
                if step.get("id") == "create-zip" and "output" in step:
                    step_output = step.get("output", {})
                    if "s3Key" in step_output:
                        found_key = step_output["s3Key"]
                        logger.info(f"Found S3 key in create-zip step output: {found_key}")
                        return found_key
            
            # If still no key, try entity reference pattern
            if "entityRef" in task_status_data.get("output", {}):
                entity_ref = task_status_data["output"]["entityRef"]
                derived_key = f"outputs/{entity_ref.replace(':', '_').replace('/', '_')}.zip"
                logger.info(f"Generated S3 key from entity ref: {derived_key}")
                return derived_key
                
        # Fallback to task ID based key
        fallback_key = f"outputs/{self.task.template_name}_{self.task_id}.zip"
        logger.info(f"Using fallback S3 key: {fallback_key}")
        return fallback_key
    
    def download_and_extract(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Download and extract a template result from S3.
        
        Returns:
            Tuple of (success, output_path, error_message)
        """
        if not self.s3_bucket or not self.local_path:
            logger.warning("S3 bucket or local path not provided, skipping download")
            return False, None, "S3 bucket or local path not provided"
            
        if not self.task_status_callback:
            logger.warning("Task status callback not provided, cannot poll for completion")
            return False, None, "Task status callback not provided"
            
        start_time = time.time()
        logger.info(f"Waiting for task {self.task_id} to complete for S3 download...")
        print(f"Waiting for task {self.task_id} to complete for S3 download...")
        
        try:
            # Poll for task completion
            while time.time() - start_time < self.timeout:
                task_status_data = self.task_status_callback(self.task_id)
                status = task_status_data.get("status", "").lower()
                logger.debug(f"Task {self.task_id} current status: {status}")
                print(f"Task {self.task_id} current status: {status}")
                
                if status == "completed":
                    logger.info(f"Task {self.task_id} completed.")
                    print(f"Task {self.task_id} completed.")
                    
                    # Determine S3 key to use
                    use_s3_key = self.determine_s3_key(task_status_data)
                    
                    if use_s3_key:
                        logger.info(f"Downloading from S3: s3://{self.s3_bucket}/{use_s3_key}")
                        print(f"Downloading from S3: s3://{self.s3_bucket}/{use_s3_key}")
                        
                        # Download the file
                        zip_file_path = self.local_path + ".zip"  # Add .zip extension for the downloaded file
                        download_success = self.s3_client.download_file(
                            bucket=self.s3_bucket,
                            key=use_s3_key,
                            local_path=zip_file_path
                        )

                        if download_success:
                            # Create a directory for extraction
                            extract_dir = self.local_path
                            # Unzip the file and delete the zip
                            unzip_success = self.s3_client.unzip_file(
                                local_zip_path=zip_file_path,
                                extract_dir=extract_dir
                            )

                            if unzip_success:
                                logger.info(f"Unzipped file to {extract_dir}")
                                print(f"Unzipped file to {extract_dir}")
                                return True, extract_dir, None
                            else:
                                error_msg = f"Failed to unzip file from S3"
                                logger.error(error_msg)
                                print(error_msg)
                                return False, None, error_msg
                        else:
                            error_msg = f"Failed to download file from S3"
                            logger.error(error_msg)
                            print(error_msg)
                            return False, None, error_msg
                    else:
                        error_msg = "No S3 key available, skipping download"
                        logger.warning(error_msg)
                        print(error_msg)
                        return False, None, error_msg
                    
                elif status in ["failed", "cancelled", "skipped"]:
                    error_msg = f"Task failed with status: {status}"
                    logger.error(f"Task {self.task_id} {error_msg}")
                    print(f"Task {self.task_id} {error_msg}")
                    return False, None, error_msg
                
                time.sleep(self.poll_interval)
                
            if time.time() - start_time >= self.timeout:
                error_msg = f"Timeout waiting for task to complete after {self.timeout} seconds"
                logger.warning(f"Timeout waiting for task {self.task_id} to complete")
                print(f"Timeout waiting for task {self.task_id} to complete")
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Error during task polling or S3 download: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
            return False, None, error_msg

        return False, None, "Unexpected error in download process" 