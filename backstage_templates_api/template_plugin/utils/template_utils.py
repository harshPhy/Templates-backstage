"""
Template Utilities

This module provides utility functions for working with templates.
"""

import os
import logging
import shutil
from typing import Dict, Any, List
import jinja2

from template_plugin.errors.exceptions import TemplateProcessingError, TemplateValidationError

logger = logging.getLogger("template-utils")

def render_template_string(template_string: str, values: Dict[str, Any]) -> str:
    """
    Render a template string with the provided values.
    
    Args:
        template_string: Template string to render
        values: Values to use for rendering
        
    Returns:
        Rendered string
        
    Raises:
        TemplateProcessingError: If there is an error processing the template
    """
    try:
        # Create a Jinja2 environment with safe defaults
        env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=True,
            undefined=jinja2.StrictUndefined
        )
        
        # Create and render the template
        template = env.from_string(template_string)
        return template.render(**values)
    except jinja2.exceptions.TemplateError as e:
        logger.error(f"Template processing error: {str(e)}")
        raise TemplateProcessingError(f"Failed to render template: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise TemplateProcessingError(f"Unexpected error: {str(e)}")

def process_template_files(source_dir: str, target_dir: str, values: Dict[str, Any]) -> None:
    """
    Process template files from source directory to target directory.
    
    Args:
        source_dir: Source directory containing template files
        target_dir: Target directory to write processed files
        values: Values to use for rendering templates
        
    Raises:
        TemplateProcessingError: If there is an error processing the templates
    """
    try:
        logger.info(f"Processing templates from {source_dir} to {target_dir}")
        
        # Ensure target directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        # Process all files and directories
        for root, dirs, files in os.walk(source_dir):
            # Create relative path for target
            rel_path = os.path.relpath(root, source_dir)
            target_path = os.path.join(target_dir, rel_path) if rel_path != '.' else target_dir
            
            # Create target directory if it doesn't exist
            os.makedirs(target_path, exist_ok=True)
            
            # Process files
            for file in files:
                source_file = os.path.join(root, file)
                
                # Determine target file name (may contain template variables)
                target_file_name = file
                if '{' in file and '}' in file:
                    target_file_name = render_template_string(file, values)
                
                target_file = os.path.join(target_path, target_file_name)
                
                # Process file contents
                if file.endswith(('.j2', '.jinja', '.jinja2', '.tmpl')):
                    # Template file - render it
                    with open(source_file, 'r') as f:
                        template_content = f.read()
                    
                    rendered_content = render_template_string(template_content, values)
                    
                    # Strip template extension if present
                    for ext in ['.j2', '.jinja', '.jinja2', '.tmpl']:
                        if target_file.endswith(ext):
                            target_file = target_file[:-len(ext)]
                            break
                    
                    # Write rendered content
                    with open(target_file, 'w') as f:
                        f.write(rendered_content)
                else:
                    # Regular file - copy it
                    shutil.copy2(source_file, target_file)
                    
        logger.info(f"Template processing complete")
        
    except TemplateProcessingError:
        raise
    except Exception as e:
        logger.error(f"Failed to process templates: {str(e)}")
        raise TemplateProcessingError(f"Failed to process templates: {str(e)}")

def validate_template_parameters(parameters: Dict[str, Any], schema: List[Dict[str, Any]]) -> None:
    """
    Validate template parameters against a schema.
    
    Args:
        parameters: Parameters to validate
        schema: Parameter schema
        
    Raises:
        TemplateValidationError: If validation fails
    """
    try:
        logger.info("Validating template parameters")
        
        # Extract required parameters from schema
        required_params = []
        for param_block in schema:
            if 'required' in param_block:
                required_params.extend(param_block['required'])
            
            # Check if parameters match property definitions
            if 'properties' in param_block:
                for param_name, param_def in param_block['properties'].items():
                    if param_name in parameters:
                        # Type validation
                        param_type = param_def.get('type')
                        if param_type == 'string' and not isinstance(parameters[param_name], str):
                            raise TemplateValidationError(f"Parameter '{param_name}' must be a string")
                        elif param_type == 'number' and not isinstance(parameters[param_name], (int, float)):
                            raise TemplateValidationError(f"Parameter '{param_name}' must be a number")
                        elif param_type == 'boolean' and not isinstance(parameters[param_name], bool):
                            raise TemplateValidationError(f"Parameter '{param_name}' must be a boolean")
                        elif param_type == 'array' and not isinstance(parameters[param_name], list):
                            raise TemplateValidationError(f"Parameter '{param_name}' must be an array")
                        elif param_type == 'object' and not isinstance(parameters[param_name], dict):
                            raise TemplateValidationError(f"Parameter '{param_name}' must be an object")
        
        # Check for missing required parameters
        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            raise TemplateValidationError(f"Missing required parameters: {', '.join(missing_params)}")
        
        logger.info("Template parameters are valid")
        
    except TemplateValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during validation: {str(e)}")
        raise TemplateValidationError(f"Unexpected error during validation: {str(e)}")
