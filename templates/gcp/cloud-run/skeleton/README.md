# GCP Cloud Run Service: ${{values.serviceName}}

${{values.description}}

This Terraform configuration creates a Google Cloud Run service with the following properties:

- **Service Name**: ${{values.serviceName}}
- **Project ID**: ${{values.projectId}}
- **Region**: ${{values.region}}
- **Container Image**: ${{values.image}}
- **CPU Allocation**: ${{values.cpu}}
- **Memory Allocation**: ${{values.memory}}
- **Max Instances**: ${{values.maxInstances}}

## Prerequisites

- Google Cloud SDK installed and configured
- Terraform installed (v1.0.0 or newer)
- Google Cloud Project with billing enabled
- IAM permissions to create and manage Cloud Run services

## Usage

1. Initialize Terraform:

   ```bash
   terraform init
   ```

2. Create a deployment plan:

   ```bash
   terraform plan
   ```

3. Apply the configuration:

   ```bash
   terraform apply
   ```

4. To destroy the resources when no longer needed:
   ```bash
   terraform destroy
   ```

## Accessing the Service

After deployment, the service will be available at the URL provided in the output. The service is configured to be publicly accessible by default.

## Custom Container Image

To deploy your own container:

1. Build and tag your container:

   ```bash
   docker build -t gcr.io/${{values.projectId}}/my-app:v1 .
   ```

2. Push to Google Container Registry:

   ```bash
   docker push gcr.io/${{values.projectId}}/my-app:v1
   ```

3. Update the `image` variable in your Terraform configuration or during template execution.
