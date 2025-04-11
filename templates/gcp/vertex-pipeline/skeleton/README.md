# GCP Vertex AI Pipeline: ${{values.pipelineName}}

${{values.description}}

This Terraform configuration creates a Google Cloud Vertex AI pipeline with the following properties:

- **Project ID**: ${{values.projectId}}
- **Pipeline Name**: ${{values.pipelineName}}
- **Region**: ${{values.region}}
- **Machine Type**: ${{values.machineType}}

## Prerequisites

- Google Cloud SDK installed and configured
- Terraform installed (v1.0.0 or newer)
- Google Cloud Project with billing enabled
- Pipeline specification file in JSON format
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

## Pipeline Specification

The pipeline specification file (`${{values.pipelineSpecPath}}`) should be a valid Vertex AI pipeline specification in JSON format. You can create this file using the Kubeflow Pipelines SDK or the TFX SDK.

### Example using Kubeflow Pipelines SDK

```python
import kfp
from kfp import dsl
from kfp.v2 import compiler
from google.cloud import aiplatform

# Define your pipeline
@dsl.pipeline(
    name="${{values.pipelineName}}",
    description="${{values.description}}"
)
def my_pipeline(project_id: str = "${{values.projectId}}",
                region: str = "${{values.region}}",
                machine_type: str = "${{values.machineType}}"):

    # Define your pipeline steps here
    preprocess_op = dsl.ContainerOp(
        name="preprocess",
        image="gcr.io/${{values.projectId}}/preprocess:latest",
        command=["python", "preprocess.py"],
        arguments=["--project", project_id, "--region", region]
    )

    train_op = dsl.ContainerOp(
        name="train",
        image="gcr.io/${{values.projectId}}/train:latest",
        command=["python", "train.py"],
        arguments=["--project", project_id, "--region", region]
    )

    train_op.after(preprocess_op)

# Compile the pipeline
compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path="${{values.pipelineSpecPath}}"
)
```

## Accessing the Pipeline

After deployment, you can view your pipeline in the Google Cloud Console:

[Vertex AI Pipelines](https://console.cloud.google.com/vertex-ai/pipelines/runs?project=${{values.projectId}})

## Monitoring and Logs

You can monitor your pipeline's performance and view logs in the Google Cloud Console:

- Pipeline runs: [Vertex AI Pipelines](https://console.cloud.google.com/vertex-ai/pipelines/runs?project=${{values.projectId}})
- Logs: [Cloud Logging](https://console.cloud.google.com/logs/query?project=${{values.projectId}})

## Next Steps

- Set up CI/CD for your pipeline using Cloud Build
- Create a schedule for your pipeline using Cloud Scheduler
- Integrate your pipeline with other Google Cloud services
