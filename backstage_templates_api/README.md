# Backstage Templates API

A FastAPI application that serves as an API for Backstage Templates, allowing you to query and filter templates based on metadata.

## Features

- Fetch templates from a Backstage instance or local files
- Filter templates by cloud provider (AWS, Azure, GCP)
- Filter templates by type (infrastructure, application, etc.)
- Filter templates by tags
- Search templates by name, description, and title
- List all available tags, owners, and cloud providers
- Automatic fallback to local files if Backstage API is unavailable

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- HTTPX
- PyYAML
- Pydantic

## Installation

1. Clone the repository
2. Install dependencies:

```bash
cd backstage_templates_api
pip install -r requirements.txt
```

## Configuration

The API can be configured using environment variables:

```bash
# API Configuration
export BACKSTAGE_API_URL=http://backstage:7007/api
export TEMPLATES_DIR=./templates
export CATALOG_FILE=./catalog-info.yaml

# For client
export BACKSTAGE_TEMPLATES_API_URL=http://localhost:8000
export BACKSTAGE_TEMPLATES_API_TOKEN=your-api-token  # Optional
```

## Running the API

```bash
cd backstage_templates_api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the API is running, you can access the Swagger UI at:

```
http://localhost:8000/docs
```

And the ReDoc documentation at:

```
http://localhost:8000/redoc
```

## API Endpoints

### Templates

- `GET /templates` - List all templates with optional filtering
- `GET /templates/{template_name}` - Get a specific template by name
- `GET /templates/filtered/cloud-provider/{provider}` - Get templates filtered by cloud provider
- `GET /templates/filtered/type/{type}` - Get templates filtered by template type
- `GET /templates/filtered/tag/{tag}` - Get templates filtered by tag
- `GET /templates/filtered/owner/{owner}` - Get templates filtered by owner

### Metadata

- `GET /tags` - List all unique tags used in templates
- `GET /owners` - List all unique owners of templates
- `GET /cloud-providers` - List all cloud providers with available templates

## Using the Python Client

The project includes a Python client for interacting with the API:

```python
# Async client
from backstage_templates_api.client import BackstageTemplatesClient, CloudProvider

async def main():
    async with BackstageTemplatesClient() as client:
        # List all templates
        templates = await client.list_templates()
        print(f"Found {templates.total_count} templates")

        # Get AWS templates
        aws_templates = await client.get_templates_by_cloud_provider(CloudProvider.AWS)
        print(f"Found {aws_templates.total_count} AWS templates")

# Synchronous client
from backstage_templates_api.client import BackstageTemplatesClientSync, CloudProvider

with BackstageTemplatesClientSync() as client:
    # List all templates
    templates = client.list_templates()
    print(f"Found {templates.total_count} templates")

    # Get AWS templates
    aws_templates = client.get_templates_by_cloud_provider(CloudProvider.AWS)
    print(f"Found {aws_templates.total_count} AWS templates")
```

## Integration with Backstage

This API can be integrated with Backstage in two ways:

1. **As a proxy**: Deploy alongside Backstage and use it to query template metadata
2. **As a standalone service**: Deploy separately and configure Backstage to use it as an external template source

### Backstage Integration Steps

1. Add the API URL to your Backstage `app-config.yaml`:

```yaml
backstage:
  templateApi:
    baseUrl: http://localhost:8000
```

2. Configure a proxy in your Backstage instance:

```yaml
proxy:
  '/templates-api':
    target: http://localhost:8000
    changeOrigin: true
    pathRewrite:
      '^/templates-api': ''
```

## License

MIT
