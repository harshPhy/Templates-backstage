"""
Backstage Templates API

This module provides a FastAPI application that serves as a REST API for interacting with
Backstage templates. It uses the template_plugin module to handle template operations.
"""

from fastapi import FastAPI, HTTPException, Query, Depends, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import logging
import sys
from model import CloudProvider, TemplateType, TemplateList, Template, TemplateTask, TemplateTaskResponse
# Import the template plugin
from template_plugin import TemplatePlugin
from template_plugin.config.config import load_config
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("backstage-templates-api")

# Initialize FastAPI
app = FastAPI(
    title="Backstage Templates API",
    description="API to interact with Backstage Templates based on metadata",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration from environment variables and/or .env file
config = load_config()

# Override config with environment variables explicitly if needed
if os.getenv("BACKSTAGE_AUTH_TOKEN"):
    config.backstage.auth_token = os.getenv("BACKSTAGE_AUTH_TOKEN")
if os.getenv("BACKSTAGE_BASE_URL"):
    config.backstage.base_url = os.getenv("BACKSTAGE_BASE_URL")
if os.getenv("LOCAL_TEMPLATES_DIR"):
    config.local.templates_dir = os.getenv("LOCAL_TEMPLATES_DIR")
if os.getenv("LOCAL_CATALOG_FILE"):
    config.local.catalog_file = os.getenv("LOCAL_CATALOG_FILE")
if os.getenv("BACKSTAGE_ENABLED"):
    config.backstage_enabled = os.getenv("BACKSTAGE_ENABLED").lower() == "true"
if os.getenv("LOCAL_ENABLED"):
    config.local_enabled = os.getenv("LOCAL_ENABLED").lower() == "true"
if os.getenv("DEFAULT_CLIENT"):
    config.default_client = os.getenv("DEFAULT_CLIENT")

# Log configuration at startup
logger.info(f"Starting Backstage Templates API with configuration:")
logger.info(f"BACKSTAGE_BASE_URL: {config.backstage.base_url}")
logger.info(f"LOCAL_TEMPLATES_DIR: {config.local.templates_dir}")
logger.info(f"LOCAL_CATALOG_FILE: {config.local.catalog_file}")
logger.info(f"BACKSTAGE_ENABLED: {config.backstage_enabled}")
logger.info(f"LOCAL_ENABLED: {config.local_enabled}")
logger.info(f"DEFAULT_CLIENT: {config.default_client}")


# Initialize the template plugin with our configuration
template_plugin = TemplatePlugin(config)

def get_template_plugin():
    """Dependency to get the template plugin instance."""
    return template_plugin

# Routes
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "healthy", "service": "backstage-templates-api"}

@app.get("/templates", response_model=TemplateList, tags=["Templates"])
async def list_templates(
    cloud_provider: Optional[CloudProvider] = Query(None, description="Filter by cloud provider"),
    template_type: Optional[TemplateType] = Query(None, description="Filter by template type"),
    tag: Optional[List[str]] = Query(None, description="Filter by tags (multiple allowed)"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    client_name: Optional[str] = Query(None, description="Name of the client to use"),
    plugin: TemplatePlugin = Depends(get_template_plugin)
):
    """
    List all available templates with optional filtering.
    """
    logger.info(f"List templates called with filters: cloud_provider={cloud_provider}, template_type={template_type}, tag={tag}, owner={owner}, search={search}, client={client_name}")
    
    try:
        templates_data = plugin.list_templates(
            cloud_provider=cloud_provider.value if cloud_provider else None,
            template_type=template_type.value if template_type else None,
            tags=tag,
            owner=owner,
            search=search,
            client_name=client_name
        )
        
        # Convert from plugin's data format to API response format
        templates_list = TemplateList(
            items=templates_data.get("items", []),
            total_count=templates_data.get("total_count", 0)
        )
        
        logger.info(f"Returning {templates_list.total_count} templates after filtering")
        return templates_list
        
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")

@app.get("/templates/{template_name}", response_model=Template, tags=["Templates"])
async def get_template(
    template_name: str,
    client_name: Optional[str] = Query(None, description="Name of the client to use"),
    plugin: TemplatePlugin = Depends(get_template_plugin)
):
    """
    Get a specific template by name.
    """
    logger.info(f"Get template called for: {template_name}")
    
    try:
        template_data = plugin.get_template(
            template_name=template_name,
            client_name=client_name
        )
        
        # Convert from plugin's data format to API response format
        template = Template.parse_obj(template_data)
        return template
        
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")

@app.get("/api-source", tags=["Health"])
async def get_api_source(plugin: TemplatePlugin = Depends(get_template_plugin)):
    """
    Return information about which data source is being used.
    """
    # Get information from the default client
    default_client = plugin.default_client
    available_clients = list(plugin.clients.keys())
    
    return {
        "default_client": default_client,
        "available_clients": available_clients,
        "backstage_enabled": config.backstage_enabled,
        "local_enabled": config.local_enabled,
        "backstage_api_url": config.backstage.base_url,
        "templates_dir": config.local.templates_dir,
        "catalog_file": config.local.catalog_file
    }

@app.post("/templates/{template_name}/execute", response_model=TemplateTaskResponse, tags=["Templates"])
async def execute_template(
    template_name: str = Path(..., description="Name of the template to execute"),
    task_request: TemplateTask = Body(..., description="Template parameters"),
    client_name: Optional[str] = Query(None, description="Name of the client to use"),
    # S3 download parameters
    s3_bucket: Optional[str] = Query(None, description="S3 bucket name for downloading result (overrides config)"),
    s3_key: Optional[str] = Query(None, description="S3 key for the generated artifact (auto-determined if not provided)"),
    local_path: Optional[str] = Query(None, description="Local path to download the artifact (uses template if not provided)"),
    aws_access_key: Optional[str] = Query(None, description="AWS access key ID (overrides config)"),
    aws_secret_key: Optional[str] = Query(None, description="AWS secret access key (overrides config)"),
    aws_region: Optional[str] = Query(None, description="AWS region (overrides config)"),
    poll_interval: Optional[int] = Query(None, description="Polling interval in seconds"),
    timeout: Optional[int] = Query(None, description="Maximum wait time in seconds"),
    plugin: TemplatePlugin = Depends(get_template_plugin)
):
    """
    Execute a template to create a component with the provided parameters.
    
    This endpoint creates a task in the Backstage scaffolder to instantiate a component
    based on the specified template and parameters.
    
    If S3 parameters are configured (either via query parameters or in config),
    this endpoint will wait for the task to complete and download the generated
    artifact from S3. The s3_key will be auto-determined if not provided.
    """
    logger.info(f"Executing template: {template_name} with parameters: {task_request.parameters}, client: {client_name}")
    
    # Log S3 download config if applicable
    if s3_bucket or (hasattr(config.backstage, 's3_bucket') and config.backstage.s3_bucket):
        logger.info(f"S3 download enabled")
    
    try:
        task_response = plugin.execute_template(
            template_name=template_name,
            parameters=task_request.parameters,
            dry_run=task_request.dry_run,
            client_name=client_name,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            local_path=local_path,
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            aws_region=aws_region,
            poll_interval=poll_interval,
            timeout=timeout
        )
        
        logger.info(f"Template execution initiated: {task_response}")
        
        # Add download information to response if available
        response_data = task_response.dict()
        if hasattr(task_response, "output_path") and task_response.output_path:
            logger.info(f"Template result downloaded to: {task_response.output_path}")
            
        return task_response
        
    except Exception as e:
        logger.error(f"Error executing template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to execute template: {str(e)}")

@app.get("/templates/{template_name}/parameters", tags=["Templates"])
async def get_template_parameters(
    template_name: str,
    client_name: Optional[str] = Query(None, description="Name of the client to use"),
    plugin: TemplatePlugin = Depends(get_template_plugin)
):
    """
    Get parameters schema for a specific template.
    
    This endpoint returns the parameters schema required to create a component
    using the specified template.
    """
    logger.info(f"Getting parameters for template: {template_name}, client: {client_name}")
    
    try:
        parameters_data = plugin.get_template_parameters(
            template_name=template_name,
            client_name=client_name
        )
        
        return parameters_data
        
    except Exception as e:
        logger.error(f"Error getting template parameters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get template parameters: {str(e)}")

@app.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task_status(
    task_id: str,
    client_name: Optional[str] = Query(None, description="Name of the client to use"),
    plugin: TemplatePlugin = Depends(get_template_plugin)
):
    """
    Get status of a task.
    
    This endpoint returns the current status of a component creation task.
    """
    logger.info(f"Getting status for task: {task_id}, client: {client_name}")
    
    try:
        task_status = plugin.get_task_status(
            task_id=task_id,
            client_name=client_name
        )
        
        return task_status
        
    except Exception as e:
        logger.error(f"Error getting task status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 