import httpx
import json
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
import os
from urllib.parse import urljoin


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

    class Config:
        allow_population_by_field_name = True


class TemplateList(BaseModel):
    items: List[Template]
    total_count: int


class BackstageTemplatesClient:
    """
    Python client for interacting with the Backstage Templates API.
    """

    def __init__(self, base_url: str = None, api_token: Optional[str] = None):
        """
        Initialize the client with base URL and optional API token.
        
        Args:
            base_url: Base URL of the API. Defaults to environment variable.
            api_token: Optional API token for authentication.
        """
        self.base_url = "http://localhost:8000"
        self.api_token = "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"
        self.client = httpx.AsyncClient(base_url=self.base_url)
        token = "eyJ0eXAiOiJ2bmQuYmFja3N0YWdlLnVzZXIiLCJhbGciOiJFUzI1NiIsImtpZCI6IjFiZjMxZjMxLTQyZjktNDMxZS1hZjMxLTQyZjktNDMxZS1hZjMxIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjcwMDcvYXBpL2F1dGgiLCJzdWIiOiJ1c2VyOmRlZmF1bHQvaGFyc2hwaHkiLCJlbnQiOlsidXNlcjpkZWZhdWx0L2hhcnNocGh5IiwiZ3JvdXA6ZGVmYXVsdC9ndWVzdHMiXSwiYXVkIjoiYmFja3N0YWdlIiwiaWF0IjoxNzQ0NjA0MjIyLCJleHAiOjE3NDQ2MDc4MjIsInVpcCI6InFlaVdkQjRuOW9nalRnLVlRbUktc1cySk9TWWQ3QzhNRm9UejNXLWJNMVJPNWdMNmo1bFF6SzhSTWQwWnpLa3FmOHBOS3poeVIwQlhTbTlHTTJaVHZRIn0.IegAgs4CR9gQ-rAx_VYHBhjU-5Im0vf1zF7I-kQJitnFh5FpQtkxdODlLS-vpTkJ4O8aCf_UkLO6ecSotHZrXQ"
        # Set authorization header if token is provided
        if self.api_token:
            self.client.headers.update({"Authorization": f"Bearer {token}"})

    async def close(self):
        """Close the HTTP client session."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request(
        self, method: str, path: str, params: Dict[str, Any] = None, json_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            json_data: JSON data for POST/PUT requests
            
        Returns:
            Response data as dictionary
        """
        url = urljoin(self.base_url, path)
        
        try:
            response = await self.client.request(
                method=method,
                url=path,
                params=params,
                json=json_data,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            raise ValueError(error_msg) from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Request error: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}") from e

    async def health_check(self) -> Dict[str, str]:
        """Check if the API is healthy."""
        return await self._request("GET", "/")

    async def list_templates(
        self,
        cloud_provider: Optional[CloudProvider] = None,
        template_type: Optional[TemplateType] = None,
        tags: Optional[List[str]] = None,
        owner: Optional[str] = None,
        search: Optional[str] = None,
    ) -> TemplateList:
        """
        List templates with optional filtering.
        
        Args:
            cloud_provider: Filter by cloud provider
            template_type: Filter by template type
            tags: Filter by tags
            owner: Filter by owner
            search: Search in name and description
            
        Returns:
            List of templates
        """
        params = {}
        if cloud_provider:
            params["cloud_provider"] = cloud_provider
        if template_type:
            params["template_type"] = template_type
        if tags:
            params["tag"] = tags
        if owner:
            params["owner"] = owner
        if search:
            params["search"] = search
            
        data = await self._request("GET", "/templates", params=params)
        return TemplateList.parse_obj(data)

    async def get_template(self, template_name: str) -> Template:
        """
        Get a specific template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template details
        """
        data = await self._request("GET", f"/templates/{template_name}")
        return Template.parse_obj(data)

    async def get_templates_by_cloud_provider(self, provider: CloudProvider) -> TemplateList:
        """
        Get templates filtered by cloud provider.
        
        Args:
            provider: Cloud provider (aws, azure, gcp)
            
        Returns:
            List of templates for the specified cloud provider
        """
        data = await self._request("GET", f"/templates/filtered/cloud-provider/{provider}")
        return TemplateList.parse_obj(data)

    async def get_templates_by_type(self, type_: TemplateType) -> TemplateList:
        """
        Get templates filtered by template type.
        
        Args:
            type_: Template type
            
        Returns:
            List of templates of the specified type
        """
        data = await self._request("GET", f"/templates/filtered/type/{type_}")
        return TemplateList.parse_obj(data)

    async def get_templates_by_tag(self, tag: str) -> TemplateList:
        """
        Get templates filtered by tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of templates with the specified tag
        """
        data = await self._request("GET", f"/templates/filtered/tag/{tag}")
        return TemplateList.parse_obj(data)

    async def get_templates_by_owner(self, owner: str) -> TemplateList:
        """
        Get templates filtered by owner.
        
        Args:
            owner: Owner to filter by
            
        Returns:
            List of templates owned by the specified owner
        """
        data = await self._request("GET", f"/templates/filtered/owner/{owner}")
        return TemplateList.parse_obj(data)

    async def list_tags(self) -> List[TemplateTag]:
        """
        List all unique tags used in templates.
        
        Returns:
            List of unique tags
        """
        data = await self._request("GET", "/tags")
        return [TemplateTag.parse_obj(item) for item in data]

    async def list_owners(self) -> List[str]:
        """
        List all unique owners of templates.
        
        Returns:
            List of unique owners
        """
        return await self._request("GET", "/owners")

    async def list_cloud_providers(self) -> List[str]:
        """
        List all cloud providers with available templates.
        
        Returns:
            List of cloud providers
        """
        return await self._request("GET", "/cloud-providers")


# Sync client using the async client
class BackstageTemplatesClientSync:
    """
    Synchronous Python client for interacting with the Backstage Templates API.
    """

    def __init__(self, base_url: str = None, api_token: Optional[str] = None):
        import asyncio
        self.base_url = "http://localhost:8000"
        self.api_token = "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"
        self._async_client = None
        self._loop = asyncio.new_event_loop()
        
    def _get_async_client(self):
        if self._async_client is None:
            self._async_client = BackstageTemplatesClient(self.base_url, self.api_token)
        return self._async_client
        
    def _run_async(self, coroutine):
        return self._loop.run_until_complete(coroutine)
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._async_client:
            self._run_async(self._async_client.close())
        self._loop.close()

    def health_check(self) -> Dict[str, str]:
        """Check if the API is healthy."""
        client = self._get_async_client()
        return self._run_async(client.health_check())

    def list_templates(
        self,
        cloud_provider: Optional[CloudProvider] = None,
        template_type: Optional[TemplateType] = None,
        tags: Optional[List[str]] = None,
        owner: Optional[str] = None,
        search: Optional[str] = None,
    ) -> TemplateList:
        """List templates with optional filtering."""
        client = self._get_async_client()
        return self._run_async(client.list_templates(
            cloud_provider=cloud_provider,
            template_type=template_type,
            tags=tags,
            owner=owner,
            search=search
        ))

    def get_template(self, template_name: str) -> Template:
        """Get a specific template by name."""
        client = self._get_async_client()
        return self._run_async(client.get_template(template_name))

    def get_templates_by_cloud_provider(self, provider: CloudProvider) -> TemplateList:
        """Get templates filtered by cloud provider."""
        client = self._get_async_client()
        return self._run_async(client.get_templates_by_cloud_provider(provider))

    def get_templates_by_type(self, type_: TemplateType) -> TemplateList:
        """Get templates filtered by template type."""
        client = self._get_async_client()
        return self._run_async(client.get_templates_by_type(type_))

    def get_templates_by_tag(self, tag: str) -> TemplateList:
        """Get templates filtered by tag."""
        client = self._get_async_client()
        return self._run_async(client.get_templates_by_tag(tag))

    def get_templates_by_owner(self, owner: str) -> TemplateList:
        """Get templates filtered by owner."""
        client = self._get_async_client()
        return self._run_async(client.get_templates_by_owner(owner))

    def list_tags(self) -> List[TemplateTag]:
        """List all unique tags used in templates."""
        client = self._get_async_client()
        return self._run_async(client.list_tags())

    def list_owners(self) -> List[str]:
        """List all unique owners of templates."""
        client = self._get_async_client()
        return self._run_async(client.list_owners())

    def list_cloud_providers(self) -> List[str]:
        """List all cloud providers with available templates."""
        client = self._get_async_client()
        return self._run_async(client.list_cloud_providers())


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def async_example():
        async with BackstageTemplatesClient() as client:
            # Check health
            health = await client.health_check()
            print(f"API Health: {health}")
            
            # List all templates
            templates = await client.list_templates()
            print(f"Found {templates.total_count} templates")
            
            # List AWS templates
            aws_templates = await client.get_templates_by_cloud_provider(CloudProvider.AWS)
            print(f"Found {aws_templates.total_count} AWS templates")
            
            # List infrastructure templates
            infra_templates = await client.get_templates_by_type(TemplateType.INFRASTRUCTURE)
            print(f"Found {infra_templates.total_count} infrastructure templates")
            
            # List tags
            tags = await client.list_tags()
            print(f"Available tags: {', '.join(tag.name for tag in tags)}")
    
    def sync_example():
        with BackstageTemplatesClientSync() as client:
            # Check health
            health = client.health_check()
            print(f"API Health: {health}")
            
            # List all templates
            templates = client.list_templates()
            print(f"Found {templates.total_count} templates")
            
            # List AWS templates
            aws_templates = client.get_templates_by_cloud_provider(CloudProvider.AWS)
            print(f"Found {aws_templates.total_count} AWS templates")
    
    # Run async example
    asyncio.run(async_example())
    
    # Run sync example
    # sync_example() 