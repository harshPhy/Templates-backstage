"""
Task Utilities

This module provides utility functions for working with template tasks.
"""

import logging
import os
from typing import Dict, Any, List, Optional

from template_plugin.clients.client_factory import ClientFactory

logger = logging.getLogger(__name__)

def get_task_logs(
    task_id: str,
    client_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get logs for a specific task.
    
    Args:
        task_id: The task ID to get logs for
        client_name: Name of the client to use (optional)
        
    Returns:
        List of log entries
    """
    client = ClientFactory.create_client(client_name)
    
    try:
        logger.info(f"Getting logs for task: {task_id}")
        
        # Use the _request method to access Backstage API directly
        response = client._request(
            method="GET",
            path=f"/scaffolder/v2/tasks/{task_id}/events"
        )
        
        # Extract and format log entries
        log_entries = []
        if "events" in response:
            for event in response["events"]:
                log_entry = {
                    "timestamp": event.get("timestamp"),
                    "type": event.get("type"),
                    "message": event.get("body", {}).get("message", ""),
                    "step": event.get("body", {}).get("stepId", ""),
                    "status": event.get("body", {}).get("status", "")
                }
                log_entries.append(log_entry)
        
        return log_entries
    except Exception as e:
        logger.error(f"Error getting task logs: {str(e)}")
        return []
        
def get_s3_key_from_logs(
    task_id: str,
    client_name: Optional[str] = None
) -> Optional[str]:
    """
    Extract S3 key from task logs.
    
    This function analyzes task logs to find the S3 key used for the template output.
    
    Args:
        task_id: The task ID
        client_name: Name of the client to use (optional)
        
    Returns:
        S3 key if found, None otherwise
    """
    logs = get_task_logs(task_id, client_name)
    
    if not logs:
        return None
    
    # Look for S3 upload message in logs
    for log in logs:
        message = log.get("message", "")
        
        # Look for messages indicating S3 uploads
        if "Uploading zip file to S3 bucket:" in message and ", key: " in message:
            # Parse the S3 key from the message
            parts = message.split(", key: ")
            if len(parts) == 2:
                return parts[1].strip()
        
        # Alternative pattern: "Zip file uploaded to S3"
        if "S3 location: s3://" in message:
            # Parse the S3 location
            parts = message.split("S3 location: s3://")
            if len(parts) == 2 and "/" in parts[1]:
                bucket_and_key = parts[1].strip()
                key_start = bucket_and_key.find('/', 0) + 1
                return bucket_and_key[key_start:]
    
    return None
        
def get_task_output(
    task_id: str,
    client_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the complete output for a task.
    
    Args:
        task_id: The task ID
        client_name: Name of the client to use (optional)
        
    Returns:
        Task output
    """
    client = ClientFactory.create_client(client_name)
    
    try:
        logger.info(f"Getting output for task: {task_id}")
        task_status = client.get_task_status(task_id)
        
        # Extract output from task status
        output = task_status.get("output", {})
        
        # Extract links from steps if available
        if "steps" in output:
            for step in output["steps"]:
                if step.get("id") == "create-zip" and "output" in step:
                    output["zip_info"] = step["output"]
        
        return output
    except Exception as e:
        logger.error(f"Error getting task output: {str(e)}")
        return {} 