from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import httpx
import os
import yaml
from enum import Enum
from datetime import datetime
import logging
import sys

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

# Configuration
class Settings:
    BACKSTAGE_API_URL: str = os.getenv("BACKSTAGE_API_URL", "http://localhost:7007/api")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "./templates")
    CATALOG_FILE: str = os.getenv("CATALOG_FILE", "./catalog-info.yaml")

settings = Settings()
auth_token = os.getenv("BACKSTAGE_AUTH_TOKEN", "eyJ0eXAiOiJ2bmQuYmFja3N0YWdlLnVzZXIiLCJhbGciOiJFUzI1NiIsImtpZCI6ImE4MDFiODY1LWUwNjktNGMyNS05YTYzLTUwNzljNzVkMGQ2OCJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjcwMDcvYXBpL2F1dGgiLCJzdWIiOiJ1c2VyOmRlZmF1bHQvaGFyc2hwaHkiLCJlbnQiOlsidXNlcjpkZWZhdWx0L2hhcnNocGh5IiwiZ3JvdXA6ZGVmYXVsdC9ndWVzdHMiXSwiYXVkIjoiYmFja3N0YWdlIiwiaWF0IjoxNzQ0NDYyMDMwLCJleHAiOjE3NDQ0NjU2MzAsInVpcCI6InAtc1BEam85LVVkbDIyNEVhakd2VWpFdktCZ082UjdkYmVLbmVnR1dvbDZ4dzBzM056Snp2cXFTNHpCUHRfSkZuRmRPeWIxa3BoYXZBeXBsT0V3YzRBIn0.vq5wmXPn88qk5uQ_2t0XkzkMioqW09r7nMZ3rMnu5h-O49N0PAZriMBXYK7PZCuJ6wcnicjvVs26zsyOx0VaJw")

# Log configuration at startup
logger.info(f"Starting Backstage Templates API with configuration:")
logger.info(f"BACKSTAGE_API_URL: {settings.BACKSTAGE_API_URL}")
logger.info(f"TEMPLATES_DIR: {settings.TEMPLATES_DIR}")
logger.info(f"CATALOG_FILE: {settings.CATALOG_FILE}")

# Enums
class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"

class TemplateType(str, Enum):
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"
    WEBSITE = "website"
    LIBRARY = "library"
    OTHER = "other"

# Models
class TemplateTag(BaseModel):
    name: str
    description: Optional[str] = None

class TemplateMetadata(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    annotations: Optional[Dict[str, str]] = None
    cloud_provider: Optional[CloudProvider] = None

class TemplateSpec(BaseModel):
    owner: str
    type: TemplateType
    templater: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None

class TemplateOutput(BaseModel):
    links: Optional[List[Dict[str, str]]] = None

class Template(BaseModel):
    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: TemplateMetadata
    spec: TemplateSpec
    output: Optional[TemplateOutput] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True

class TemplateList(BaseModel):
    items: List[Template]
    total_count: int

class ErrorResponse(BaseModel):
    error: str
    status_code: int
    detail: Optional[str] = None

# Helper functions
async def get_backstage_client():
    logger.info(f"Creating Backstage client with base URL: {settings.BACKSTAGE_API_URL}")
    
    headers = {}
    if auth_token:
        logger.info("Using authentication token for Backstage API")
        headers["Authorization"] = f"Bearer {auth_token}"
    else:
        logger.warning("No authentication token provided for Backstage API. Requests may fail with 401 Unauthorized.")
    
    async with httpx.AsyncClient(
        base_url=settings.BACKSTAGE_API_URL,
        headers=headers
    ) as client:
        yield client

async def load_template_from_file(file_path: str) -> Template:
    try:
        logger.info(f"Loading template from file: {file_path}")
        with open(file_path, 'r') as f:
            template_data = yaml.safe_load(f)
            
        # Extract cloud provider from file path or tags
        cloud_provider = None
        if "/aws/" in file_path:
            cloud_provider = CloudProvider.AWS
        elif "/azure/" in file_path:
            cloud_provider = CloudProvider.AZURE
        elif "/gcp/" in file_path:
            cloud_provider = CloudProvider.GCP
            
        # Enhance metadata with cloud provider
        if 'metadata' in template_data:
            template_data['metadata']['cloud_provider'] = cloud_provider
            
        return Template.parse_obj(template_data)
    except Exception as e:
        logger.error(f"Failed to load template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to load template: {str(e)}")

# Routes
@app.get("/", tags=["Health"])
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy", "service": "backstage-templates-api"}

@app.get("/templates", response_model=TemplateList, tags=["Templates"])
async def list_templates(
    cloud_provider: Optional[CloudProvider] = Query(None, description="Filter by cloud provider"),
    template_type: Optional[TemplateType] = Query(None, description="Filter by template type"),
    tag: Optional[List[str]] = Query(None, description="Filter by tags (multiple allowed)"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    backstage_client: httpx.AsyncClient = Depends(get_backstage_client)
):
    """
    List all available templates with optional filtering.
    """
    logger.info(f"List templates called with filters: cloud_provider={cloud_provider}, template_type={template_type}, tag={tag}, owner={owner}, search={search}")
    
    try:
        # Try to get templates from Backstage API first
        logger.info(f"Attempting to fetch templates from Backstage API: {settings.BACKSTAGE_API_URL}")
        response = await backstage_client.get("/catalog/entities?filter=kind=Template")

        if response.status_code == 200:
            logger.info(f"Successfully fetched templates from Backstage API")
            api_templates = response.json()
            templates = []
            
            for api_template in api_templates:
                # Extract and map fields from Backstage API response
                template_data = {
                    "apiVersion": api_template.get("apiVersion", "scaffolder.backstage.io/v1beta3"),
                    "kind": api_template.get("kind", "Template"),
                    "metadata": {
                        "name": api_template.get("metadata", {}).get("name", ""),
                        "title": api_template.get("spec", {}).get("title", ""),
                        "description": api_template.get("metadata", {}).get("description", ""),
                        "tags": api_template.get("metadata", {}).get("tags", []),
                        "annotations": api_template.get("metadata", {}).get("annotations", {}),
                    },
                    "spec": {
                        "owner": api_template.get("spec", {}).get("owner", ""),
                        "type": api_template.get("spec", {}).get("type", "other"),
                        "templater": api_template.get("spec", {}).get("templater", "v1beta3"),
                        "parameters": api_template.get("spec", {}).get("parameters", []),
                    },
                    "output": {
                        "links": api_template.get("spec", {}).get("output", {}).get("links", []),
                    }
                }
                
                # Try to determine cloud provider from tags or annotations
                if "aws" in template_data["metadata"].get("tags", []):
                    template_data["metadata"]["cloud_provider"] = CloudProvider.AWS
                elif "azure" in template_data["metadata"].get("tags", []):
                    template_data["metadata"]["cloud_provider"] = CloudProvider.AZURE
                elif "gcp" in template_data["metadata"].get("tags", []):
                    template_data["metadata"]["cloud_provider"] = CloudProvider.GCP
                
                template = Template.parse_obj(template_data)
                templates.append(template)
        else:
            # Fallback to local file loading if Backstage API is not available
            logger.warning(f"Failed to fetch templates from Backstage API. Status code: {response.status_code}. Falling back to local files.")
            templates = await load_templates_from_catalog()
    
    except httpx.RequestError as e:
        # Handle connection errors (e.g., Backstage API not available)
        logger.warning(f"Connection error to Backstage API: {str(e)}. Falling back to local files.")
        templates = await load_templates_from_catalog()
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")
    
    # Apply filters
    filtered_templates = templates
    
    if cloud_provider:
        filtered_templates = [t for t in filtered_templates if t.metadata.cloud_provider == cloud_provider]
    
    if template_type:
        filtered_templates = [t for t in filtered_templates if t.spec.type == template_type]
    
    if tag:
        filtered_templates = [t for t in filtered_templates if t.metadata.tags and all(t in t.metadata.tags for t in tag)]
    
    if owner:
        filtered_templates = [t for t in filtered_templates if t.spec.owner == owner]
    
    if search:
        search = search.lower()
        filtered_templates = [
            t for t in filtered_templates 
            if (search in t.metadata.name.lower() or 
                (t.metadata.description and search in t.metadata.description.lower()) or
                (t.metadata.title and search in t.metadata.title.lower()))
        ]
    
    logger.info(f"Returning {len(filtered_templates)} templates after filtering")
    return TemplateList(items=filtered_templates, total_count=len(filtered_templates))

async def load_templates_from_catalog():
    """
    Load templates from the local catalog-info.yaml file.
    """
    logger.info(f"Loading templates from local catalog file: {settings.CATALOG_FILE}")
    templates = []
    try:
        with open(settings.CATALOG_FILE, 'r') as f:
            catalog_data = yaml.safe_load(f)
        
        if catalog_data.get('kind') == 'Location' and 'spec' in catalog_data and 'targets' in catalog_data['spec']:
            template_paths = catalog_data['spec']['targets']
            logger.info(f"Found {len(template_paths)} template paths in catalog file")
            
            for path in template_paths:
                if path.endswith('template.yaml'):
                    full_path = os.path.join(os.path.dirname(settings.CATALOG_FILE), path)
                    try:
                        template = await load_template_from_file(full_path)
                        templates.append(template)
                    except Exception as e:
                        logger.error(f"Error loading template {path}: {str(e)}")
        else:
            logger.warning(f"Catalog file doesn't have the expected structure")
    except Exception as e:
        logger.error(f"Error loading catalog: {str(e)}")
    
    logger.info(f"Loaded {len(templates)} templates from local files")
    return templates

@app.get("/templates/{template_name}", response_model=Template, tags=["Templates"])
async def get_template(
    template_name: str,
    backstage_client: httpx.AsyncClient = Depends(get_backstage_client)
):
    """
    Get a specific template by name.
    """
    logger.info(f"Get template called for: {template_name}")
    
    try:
        # Try to get from Backstage API first
        logger.info(f"Attempting to fetch template from Backstage API: {template_name}")
        response = await backstage_client.get(f"/catalog/entities/by-name/template/default/{template_name}")
        
        if response.status_code == 200:
            logger.info(f"Successfully fetched template from Backstage API: {template_name}")
            api_template = response.json()
            template_data = {
                "apiVersion": api_template.get("apiVersion", "scaffolder.backstage.io/v1beta3"),
                "kind": api_template.get("kind", "Template"),
                "metadata": {
                    "name": api_template.get("metadata", {}).get("name", ""),
                    "title": api_template.get("spec", {}).get("title", ""),
                    "description": api_template.get("metadata", {}).get("description", ""),
                    "tags": api_template.get("metadata", {}).get("tags", []),
                    "annotations": api_template.get("metadata", {}).get("annotations", {}),
                },
                "spec": {
                    "owner": api_template.get("spec", {}).get("owner", ""),
                    "type": api_template.get("spec", {}).get("type", "other"),
                    "templater": api_template.get("spec", {}).get("templater", "v1beta3"),
                    "parameters": api_template.get("spec", {}).get("parameters", []),
                },
                "output": {
                    "links": api_template.get("spec", {}).get("output", {}).get("links", []),
                }
            }
            
            # Try to determine cloud provider from tags or annotations
            if "aws" in template_data["metadata"].get("tags", []):
                template_data["metadata"]["cloud_provider"] = CloudProvider.AWS
            elif "azure" in template_data["metadata"].get("tags", []):
                template_data["metadata"]["cloud_provider"] = CloudProvider.AZURE
            elif "gcp" in template_data["metadata"].get("tags", []):
                template_data["metadata"]["cloud_provider"] = CloudProvider.GCP
                
            return Template.parse_obj(template_data)
        else:
            # Fallback to local file search
            logger.warning(f"Failed to fetch template from Backstage API. Status code: {response.status_code}. Falling back to local files.")
            templates = await load_templates_from_catalog()
            for template in templates:
                if template.metadata.name == template_name:
                    return template
                    
            logger.error(f"Template not found: {template_name}")
            raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    
    except httpx.RequestError as e:
        # Fallback to local file search if Backstage API is not available
        logger.warning(f"Connection error to Backstage API: {str(e)}. Falling back to local files.")
        templates = await load_templates_from_catalog()
        for template in templates:
            if template.metadata.name == template_name:
                return template
                
        logger.error(f"Template not found: {template_name}")
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve template: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 