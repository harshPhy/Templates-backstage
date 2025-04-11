# Backstage Terraform Templates

This repository contains a collection of Terraform templates for use with Backstage Software Templates. These templates help provision cloud infrastructure across AWS, Azure, and GCP in a standardized, repeatable way.

## Integration with Backstage

### Prerequisites

1. A running Backstage instance
2. Software Templates plugin installed and configured
3. Required permissions for cloud providers (AWS, Azure, GCP)

### Integration Steps

1. **Register the Template Location**:

   ```yaml
   # app-config.yaml
   catalog:
     locations:
       - type: url
         target: https://github.com/YOUR_ORG/YOUR_REPO/blob/main/catalog-info.yaml
         rules:
           - allow: [Template]
   ```

2. **Configure Cloud Provider and GitHub Credentials**:

   ```yaml
   # app-config.yaml
   scaffolder:
     # GitHub configuration
     github:
       token: ${GITHUB_TOKEN}
       visibility: public # or private
       domain: github.com

     # Cloud provider credentials
     azure:
       credentials:
         clientId: ${AZURE_CLIENT_ID}
         clientSecret: ${AZURE_CLIENT_SECRET}
         tenantId: ${AZURE_TENANT_ID}
     aws:
       credentials:
         accessKeyId: ${AWS_ACCESS_KEY_ID}
         secretAccessKey: ${AWS_SECRET_ACCESS_KEY}
         region: ${AWS_REGION}
     gcp:
       credentials:
         application_credentials: ${GOOGLE_APPLICATION_CREDENTIALS}
         project_id: ${GOOGLE_PROJECT_ID}

   # Terraform backend configuration
   terraform:
     backend:
       # Default backend configuration
       default:
         type: s3 # or azurerm, gcs
         config:
           bucket: ${TERRAFORM_STATE_BUCKET}
           region: ${AWS_REGION}
           key: terraform.tfstate
           encrypt: true

       # Provider-specific backends
       providers:
         aws:
           type: s3
           config:
             bucket: ${AWS_TERRAFORM_BUCKET}
             region: ${AWS_REGION}
         azure:
           type: azurerm
           config:
             storage_account_name: ${AZURE_STORAGE_ACCOUNT}
             container_name: ${AZURE_CONTAINER_NAME}
         gcp:
           type: gcs
           config:
             bucket: ${GCP_TERRAFORM_BUCKET}

   # Authentication configuration
   auth:
     environment: production
     providers:
       github:
         development:
           clientId: ${AUTH_GITHUB_CLIENT_ID}
           clientSecret: ${AUTH_GITHUB_CLIENT_SECRET}
   ```

3. **Enable Required Backstage Plugins**:
   ```typescript
   // packages/app/src/plugins.ts
   export { scaffolderPlugin } from '@backstage/plugin-scaffolder';
   export { catalogPlugin } from '@backstage/plugin-catalog';
   ```

### Accessing Templates

1. **Via Backstage UI**:

   - Navigate to `Create` in your Backstage instance
   - Select from available templates:
     - AWS Templates (Lambda, SageMaker, etc.)
     - Azure Templates (Functions, ML Pipeline, etc.)
     - GCP Templates (Cloud Run, Vertex AI, etc.)

2. **Via Backstage API**:

   ```bash
   # List available templates
   curl -X GET http://your-backstage-instance/api/catalog/templates

   # Get template by name
   curl -X GET http://your-backstage-instance/api/catalog/templates/terraform-aws-lambda
   ```

### Usage Example

1. **Select Template**:

   - Go to Backstage's Create Component page
   - Choose a template (e.g., AWS Lambda)

2. **Fill Template Form**:

   ```yaml
   # Example: AWS Lambda
   functionName: my-lambda
   runtime: nodejs18.x
   handler: index.handler
   memorySize: 128
   timeout: 30
   ```

3. **Generate Infrastructure**:
   - Click "Create" to generate Terraform configuration
   - Follow deployment instructions in generated README

### Template Parameters

Each template accepts specific parameters:

**AWS Lambda**:

- `functionName`: Name of the Lambda function
- `runtime`: Runtime environment (nodejs, python, etc.)
- `handler`: Function handler path
- `memorySize`: Memory allocation in MB
- `timeout`: Function timeout in seconds

**Azure ML Pipeline**:

- `workspaceName`: Azure ML workspace name
- `pipelineName`: Name of the ML pipeline
- `location`: Azure region
- `computeType`: Compute target type

**GCP Cloud Run**:

- `serviceName`: Name of the Cloud Run service
- `region`: GCP region
- `image`: Container image to deploy
- `memory`: Memory allocation

## Troubleshooting

Common issues and solutions:

1. **Template Not Appearing**:

   - Verify catalog-info.yaml is correctly registered
   - Check Backstage logs for registration errors
   - Ensure template follows Backstage schema

2. **Permission Errors**:

   - Verify cloud provider credentials
   - Check required IAM roles/permissions
   - Ensure environment variables are set

3. **Terraform Errors**:
   - Verify Terraform installation
   - Check provider configurations
   - Validate input parameters

## Security Considerations

1. **Credential Management**:

   - Use environment variables for secrets
   - Implement proper IAM roles
   - Rotate credentials regularly

2. **Access Control**:
   - Configure RBAC in Backstage
   - Limit template access by teams
   - Audit template usage

## Support and Maintenance

For issues or contributions:

1. Open an issue in the repository
2. Follow contribution guidelines
3. Contact platform team for urgent issues

## References

- [Backstage Documentation](https://backstage.io/docs)
- [Software Templates](https://backstage.io/docs/features/software-templates)
- [Terraform Documentation](https://www.terraform.io/docs)
- [Cloud Provider Docs](https://backstage.io/docs/integrations)

## Overview

The templates in this repository follow a consistent structure and are designed to be used with Backstage's Software Templates feature. Each template provides infrastructure-as-code definitions using Terraform to create and manage cloud resources.

## Cloud Providers and Templates

### AWS

- **Lambda Function**: Serverless functions for event-driven applications
- **SageMaker Endpoint**: ML model deployment endpoints
- **SageMaker Pipeline**: ML workflow orchestration pipelines
- **Spark Pipeline**: Big data processing with EMR
- **SNS Topic**: Messaging and notifications

### Azure

- **Function Endpoint**: Serverless functions in Azure
- **ML Pipeline**: Machine learning pipelines in Azure ML
- **Spark Pipeline**: Spark workloads with Azure Databricks
- **Kubeflow Pipeline**: ML pipelines with Kubeflow on AKS

### GCP

- **Cloud Run**: Fully managed serverless container platform
- **Vertex Pipeline**: ML workflows with Vertex AI
- **Dataflow Pipeline**: Streaming and batch data processing
- **Kubeflow Pipeline**: ML pipelines with Kubeflow on GKE

## Template Structure

Each template follows a consistent structure:

```
templates/<cloud-provider>/<service-name>/
├── template.yaml        # Template definition for Backstage
└── skeleton/           # Files that will be templated
    ├── main.tf         # Terraform main configuration
    ├── variables.tf    # Input variables for Terraform
    ├── outputs.tf      # Output values after deployment
    ├── catalog-info.yaml # Backstage catalog entity definition
    └── README.md       # Usage instructions
```

## Using the Templates

1. Ensure Backstage is set up with the Software Templates plugin
2. Register these templates in your Backstage instance
3. Select a template from the Backstage "Create" page
4. Fill in the required parameters
5. Generate the project
6. Follow the deployment instructions in the generated code

## Template Features

- **Consistent Structure**: All templates follow the same organizational pattern
- **Backstage Integration**: Templates include catalog-info.yaml for automatic registration
- **Parameterized**: Customizable through template parameters
- **Documentation**: Each template includes usage instructions
- **Best Practices**: Templates implement cloud provider best practices

## Catalog Integration

All templates include a `catalog-info.yaml` file that uses the `${{ values.xxx }}` notation to incorporate template parameter values. This enables automatic registration in the Backstage catalog with correct metadata, annotations, and relationships.

## Contributing

To add a new template:

1. Create a new folder under the appropriate cloud provider
2. Add a `template.yaml` file with the template definition
3. Create a `skeleton` folder with the Terraform files and other resources
4. Include a `catalog-info.yaml` for Backstage integration
5. Add documentation in a README.md file

## Additional Backstage Configuration

### 1. Install Required Dependencies

Add these to your Backstage app's `package.json`:

```json
{
  "dependencies": {
    "@backstage/plugin-scaffolder-backend-module-terraform": "^1.0.0",
    "@backstage/plugin-terraform": "^0.1.0",
    "@backstage/plugin-kubernetes": "^0.1.0"
  }
}
```

### 2. Configure Backend

In your `packages/backend/src/plugins/scaffolder.ts`:

```typescript
import { ScaffolderEntitiesProcessor } from '@backstage/plugin-scaffolder-backend';
import { TerraformGenerator } from '@backstage/plugin-scaffolder-backend-module-terraform';

export default async function createPlugin(
  env: PluginEnvironment
): Promise<Router> {
  const scaffolder = await createRouter({
    actions: [
      createBuiltinActions({
        containerRunner,
        integrations,
        config: env.config,
        catalogClient: env.catalogClient,
        reader: env.reader,
      }),
      TerraformGenerator(), // Add Terraform generator
    ],
    catalogClient: env.catalogClient,
    logger: env.logger,
    config: env.config,
    database: env.database,
    reader: env.reader,
  });

  return scaffolder;
}
```

### 3. Add Required Plugins to Your Backstage Instance

In `packages/app/src/App.tsx`:

```typescript
import { TerraformPage } from '@backstage/plugin-terraform';
import { KubernetesPage } from '@backstage/plugin-kubernetes';

const routes = (
  <FlatRoutes>
    {/* ... other routes ... */}
    <Route path="/terraform" element={<TerraformPage />} />
    <Route path="/kubernetes" element={<KubernetesPage />} />
  </FlatRoutes>
);
```

### 4. Configure RBAC (Optional but Recommended)

In your `app-config.yaml`:

```yaml
permission:
  rbac:
    roles:
      - name: terraform-admin
        permissions:
          - policy: 'catalog-entity'
            effect: allow
            resourceType: 'template'
            conditions:
              - field: 'kind'
                value: 'Template'
              - field: 'metadata.tags'
                value: 'terraform'
      - name: infrastructure-deployer
        permissions:
          - policy: 'scaffolder'
            effect: allow
            resourceType: 'template'
            conditions:
              - field: 'metadata.tags'
                value: 'terraform'
```

### 5. Add Template Discovery (Optional)

To automatically discover new templates:

```yaml
# app-config.yaml
catalog:
  rules:
    - allow: [Component, API, Resource, Location, Template]
  locations:
    - type: url
      target: https://github.com/YOUR_ORG/YOUR_REPO/blob/main/catalog-info.yaml
      rules:
        - allow: [Template]
    - type: url
      target: https://github.com/YOUR_ORG/YOUR_REPO/blob/main/templates/*/*/template.yaml
      rules:
        - allow: [Template]
```

### 6. Configure Terraform Backend (Recommended)

Add a default Terraform backend configuration:

```yaml
# app-config.yaml
scaffolder:
  terraform:
    defaultBackend:
      type: s3 # or azurerm, gcs
      config:
        bucket: your-terraform-state-bucket
        region: us-west-2
```

### 7. Add Template Validation (Optional)

Create a template validation workflow:

```yaml
# .github/workflows/template-validation.yml
name: Template Validation
on:
  pull_request:
    paths:
      - 'templates/**'
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Templates
        uses: backstage/backstage-cli@main
        with:
          args: template:verify --path templates
```

### 8. Monitor Template Usage (Optional)

Enable template usage analytics:

```yaml
# app-config.yaml
backend:
  analytics:
    enabled: true
    implementations:
      - name: google-analytics
        config:
          trackingId: 'YOUR-GA-TRACKING-ID'
```
