"""
File Utilities

This module provides utility functions for working with files and directories.
"""

import os
import logging
import shutil
import yaml
from typing import List, Dict, Any, Optional

from template_plugin.errors.exceptions import FileAccessError

logger = logging.getLogger("file-utils")

def find_file(directory: str, filename: str) -> Optional[str]:
    """
    Find a file in a directory and its subdirectories.
    
    Args:
        directory: Directory to search in
        filename: Filename to find
        
    Returns:
        Full path to the file if found, None otherwise
    """
    try:
        logger.debug(f"Finding file '{filename}' in '{directory}'")
        
        for root, dirs, files in os.walk(directory):
            if filename in files:
                filepath = os.path.join(root, filename)
                logger.debug(f"Found file: {filepath}")
                return filepath
        
        logger.debug(f"File '{filename}' not found in '{directory}'")
        return None
    except Exception as e:
        logger.error(f"Error finding file: {str(e)}")
        return None

def read_yaml_file(filepath: str) -> Dict[str, Any]:
    """
    Read and parse a YAML file.
    
    Args:
        filepath: Path to the YAML file
        
    Returns:
        Parsed YAML content
        
    Raises:
        FileAccessError: If there is an error reading or parsing the file
    """
    try:
        logger.debug(f"Reading YAML file: {filepath}")
        
        with open(filepath, 'r') as f:
            content = yaml.safe_load(f)
            
        if content is None:
            # Empty file
            return {}
            
        return content
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error in {filepath}: {str(e)}")
        raise FileAccessError(f"Failed to parse YAML file '{filepath}': {str(e)}")
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {str(e)}")
        raise FileAccessError(f"Failed to read file '{filepath}': {str(e)}")

def write_yaml_file(filepath: str, data: Dict[str, Any]) -> None:
    """
    Write data to a YAML file.
    
    Args:
        filepath: Path to the YAML file
        data: Data to write
        
    Raises:
        FileAccessError: If there is an error writing the file
    """
    try:
        logger.debug(f"Writing YAML file: {filepath}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
            
    except yaml.YAMLError as e:
        logger.error(f"YAML formatting error: {str(e)}")
        raise FileAccessError(f"Failed to format YAML for file '{filepath}': {str(e)}")
    except Exception as e:
        logger.error(f"Error writing file {filepath}: {str(e)}")
        raise FileAccessError(f"Failed to write file '{filepath}': {str(e)}")

def list_directories(directory: str) -> List[str]:
    """
    List subdirectories in a directory.
    
    Args:
        directory: Directory to list subdirectories of
        
    Returns:
        List of subdirectory names
        
    Raises:
        FileAccessError: If there is an error listing the directory
    """
    try:
        logger.debug(f"Listing directories in: {directory}")
        
        if not os.path.exists(directory):
            logger.warning(f"Directory does not exist: {directory}")
            return []
            
        return [d for d in os.listdir(directory) 
                if os.path.isdir(os.path.join(directory, d))]
    except Exception as e:
        logger.error(f"Error listing directory {directory}: {str(e)}")
        raise FileAccessError(f"Failed to list directory '{directory}': {str(e)}")

def copy_directory(source: str, destination: str) -> None:
    """
    Copy a directory and its contents to a destination.
    
    Args:
        source: Source directory
        destination: Destination directory
        
    Raises:
        FileAccessError: If there is an error copying the directory
    """
    try:
        logger.debug(f"Copying directory from {source} to {destination}")
        
        if not os.path.exists(source):
            raise FileAccessError(f"Source directory does not exist: {source}")
            
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(os.path.abspath(destination)), exist_ok=True)
        
        # Copy directory
        shutil.copytree(source, destination, dirs_exist_ok=True)
        
    except FileAccessError:
        raise
    except Exception as e:
        logger.error(f"Error copying directory from {source} to {destination}: {str(e)}")
        raise FileAccessError(f"Failed to copy directory: {str(e)}")
