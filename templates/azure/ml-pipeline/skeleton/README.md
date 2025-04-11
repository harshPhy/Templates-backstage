# Azure ML Pipeline: ${{values.pipelineName}}

${{values.description}}

This Terraform configuration creates an Azure Machine Learning workspace and compute cluster with the following properties:

- **Workspace Name**: ${{values.workspaceName}}
- **Pipeline Name**: ${{values.pipelineName}}
- **Location**: ${{values.location}}
- **Compute Type**: ${{values.computeType}}
- **VM Size**: ${{values.vmSize}}

## Prerequisites

- Azure CLI installed and configured
- Terraform installed (v1.0.0 or newer)
- Azure subscription with appropriate permissions

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

## Next Steps

After deploying this infrastructure, you can create your ML pipeline using:

1. Azure Machine Learning SDK for Python
2. Azure Machine Learning Studio UI
3. Azure DevOps ML Pipelines

Example pipeline definition in Python:

```python
from azureml.core import Workspace, Experiment, Environment
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep

# Connect to workspace
ws = Workspace.get(
    name="${{values.workspaceName}}",
    subscription_id="your-subscription-id",
    resource_group="${{values.workspaceName}}-rg"
)

# Create a pipeline step
step1 = PythonScriptStep(
    name="data-prep",
    script_name="prep.py",
    compute_target="${{values.workspaceName}}-compute",
    source_directory="./scripts"
)

# Create the pipeline
pipeline = Pipeline(workspace=ws, steps=[step1])

# Submit the pipeline
pipeline_run = pipeline.submit("${{values.pipelineName}}")
```
