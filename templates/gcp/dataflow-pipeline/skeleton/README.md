# GCP Dataflow Pipeline: ${{values.jobName}}

This Terraform configuration creates a Google Dataflow pipeline for data processing with the following properties:

- **Project ID**: ${{values.projectId}}
- **Job Name**: ${{values.jobName}}
- **Region**: ${{values.region}}
- **Machine Type**: ${{values.machineType}}
- **Max Workers**: ${{values.maxWorkers}}

## Prerequisites

- Google Cloud SDK installed and configured
- Terraform installed (v1.0.0 or newer)
- Google Cloud Project with billing enabled
- Dataflow template available in GCS
- Appropriate permissions to create resources in the project

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

## Dataflow Template

This configuration requires a Dataflow template stored in Google Cloud Storage at `${{values.templatePath}}`. Google provides several pre-built templates for common data processing tasks, or you can create your own custom template.

### Using Pre-built Templates

Google Cloud provides many pre-built templates for common data processing tasks. Here are some examples:

1. Text Files on Cloud Storage to BigQuery:

   ```
   gs://dataflow-templates/latest/GCS_Text_to_BigQuery
   ```

2. Pub/Sub to BigQuery:

   ```
   gs://dataflow-templates/latest/PubSub_to_BigQuery
   ```

3. Pub/Sub to Cloud Storage:
   ```
   gs://dataflow-templates/latest/PubSub_to_GCS_Text
   ```

### Creating Custom Templates

You can create your own custom templates using the Apache Beam SDK:

1. Write your pipeline code in Java, Python, or Go
2. Create a template spec
3. Build and upload your template to Google Cloud Storage

## Monitoring and Logs

You can monitor your pipeline's performance and view logs in the Google Cloud Console:

- Pipeline jobs: [Dataflow Jobs](https://console.cloud.google.com/dataflow/jobs)
- Logs: [Cloud Logging](https://console.cloud.google.com/logs/query)

## Common Pipeline Parameters

When using this template, you may need to provide additional parameters specific to your template. These can be added to the `parameters` block in the `main.tf` file.

For example, for the GCS to BigQuery template, you might add:

```
parameters = {
  inputFilePattern = "gs://your-bucket/path/to/data/*.csv"
  outputTable = "your-project:your-dataset.your-table"
  serviceAccount = google_service_account.dataflow_service_account.email
}
```
