# AWS SageMaker Pipeline: ${{values.pipelineName}}

${{values.description}}

This Terraform configuration creates an AWS SageMaker pipeline for MLOps/LLMOps with the following properties:

- **Pipeline Name**: ${{values.pipelineName}}
- **Pipeline Type**: ${{values.pipelineDefinition}}
- **Instance Type**: ${{values.instanceType}}

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)
- IAM role with appropriate permissions for SageMaker
- Training and inference container images in Amazon ECR (for custom pipelines)

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

## Pipeline Structure

{{#eq values.pipelineDefinition "training"}}
This pipeline consists of the following steps:

1. **Training Step**: Trains a machine learning model using the specified training data
2. **Create Model Step**: Creates a model from the trained artifacts

You can execute this pipeline with different parameters to train models on different datasets.
{{/eq}}

{{#eq values.pipelineDefinition "processing"}}
This pipeline consists of a data processing step that prepares data for machine learning.
{{/eq}}

{{#eq values.pipelineDefinition "inference"}}
This pipeline creates an inference pipeline with preprocessing and postprocessing steps.
{{/eq}}

{{#eq values.pipelineDefinition "custom"}}
This is a custom pipeline. Review the pipeline definition for details on its structure and functionality.
{{/eq}}

## Executing the Pipeline

To execute the pipeline using AWS CLI:

```bash
aws sagemaker start-pipeline-execution \
  --pipeline-name ${{values.pipelineName}} \
  --pipeline-parameters '[{"Name":"InputDataUrl","Value":"s3://your-bucket/your-data"}]'
```

## Monitoring Pipeline Executions

You can monitor pipeline executions in the AWS SageMaker Console:
[SageMaker Pipelines Console](https://console.aws.amazon.com/sagemaker/home#/pipelines)
