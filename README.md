# Backstage Terraform Templates

This repository contains a collection of Terraform templates for use with Backstage Software Templates. These templates help provision cloud infrastructure across AWS, Azure, and GCP in a standardized, repeatable way.

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
