# Backstage Templates API

A Python-based API for interacting with Backstage Software Templates, providing a flexible and extensible way to manage and deploy templates across different environments.

## Features

- **Multiple Client Support**: Supports both Backstage and Local template clients
- **S3 Integration**: Built-in support for downloading template results from S3
- **Flexible Configuration**: Environment-based configuration with sensible defaults
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive error handling and logging

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The API can be configured through environment variables or a configuration file:

### Environment Variables

```bash
# Backstage Configuration
BACKSTAGE_URL=https://backstage.example.com/api
BACKSTAGE_TOKEN=your-token

# S3 Configuration
TEMPLATE_S3_BUCKET=my-templates-bucket
BACKSTAGE_AWS_ACCESS_KEY=your-access-key
BACKSTAGE_AWS_SECRET_KEY=your-secret-key
BACKSTAGE_AWS_REGION=us-west-2

# Local Configuration
LOCAL_TEMPLATES_DIR=/path/to/templates
LOCAL_CATALOG_FILE=catalog-info.yaml
```

### Configuration File

```python
from template_plugin.config.config import ClientsConfig

config = ClientsConfig(
    backstage_enabled=True,
    local_enabled=True,
    default_client="backstage",
    backstage={
        "base_url": "https://backstage.example.com/api",
        "auth_token": "your-token"
    },
    local={
        "templates_dir": "/path/to/templates",
        "catalog_file": "catalog-info.yaml"
    }
)
```

## Usage

### Basic Usage

```python
from template_plugin.template_plugin import TemplatePlugin

# Initialize the plugin
plugin = TemplatePlugin()

# List available templates
templates = plugin.list_templates()

# Get template details
template = plugin.get_template("my-template")

# Get template parameters
parameters = plugin.get_template_parameters("my-template")

# Execute a template
response = plugin.execute_template(
    template_name="my-template",
    parameters={
        "name": "my-service",
        "description": "A new service"
    }
)
```

## API Reference

### TemplatePlugin

The main class for interacting with templates:

- `__init__(config: Optional[Union[TemplatePluginConfig, ClientsConfig]] = None)`
- `list_templates(cloud_provider: Optional[str] = None, ...) -> Dict[str, Any]`
- `get_template(template_name: str, ...) -> Dict[str, Any]`
- `get_template_parameters(template_name: str, ...) -> Dict[str, Any]`
- `execute_template(template_name: str, parameters: Dict[str, Any], ...) -> TemplateTaskResponse`
- `get_task_status(task_id: str, ...) -> Dict[str, Any]`

## Error Handling

The API provides comprehensive error handling through custom exceptions:

- `TemplateError`: Base class for template-related errors
- `TemplateNotFoundError`: Template not found
- `TemplateExecutionError`: Error during template execution
- `ClientInitializationError`: Error initializing template clients
- `ConnectionError`: Connection-related errors

## Logging

The API uses Python's logging module with the following loggers:

- `template-plugin`: Main plugin logger
- `backstage-template-client`: Backstage client logger
- `s3-client`: S3 client logger

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
