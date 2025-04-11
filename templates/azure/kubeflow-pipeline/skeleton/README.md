# Azure Kubeflow Pipeline: ${{values.clusterName}}

This Terraform configuration deploys Kubeflow Pipelines on Azure Kubernetes Service (AKS) with the following properties:

- **Resource Group**: ${{values.resourceGroupName}}
- **Cluster Name**: ${{values.clusterName}}
- **Location**: ${{values.location}}
- **Kubernetes Version**: ${{values.kubernetesVersion}}
- **VM Size**: ${{values.vmSize}}
- **Node Count**: ${{values.nodeCount}}
- **Kubeflow Version**: ${{values.kubeflowVersion}}

## Prerequisites

- Azure CLI installed and configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)
- kubectl installed
- Helm installed
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

## Connecting to the Cluster

After the deployment is complete, you can connect to the cluster using kubectl:

```bash
az aks get-credentials --resource-group ${{values.resourceGroupName}} --name ${{values.clusterName}}
```

## Accessing Kubeflow UI

By default, Kubeflow UI is deployed without external access. You can use port forwarding to access it:

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Then open your browser and navigate to: [http://localhost:8080](http://localhost:8080)

## Creating a Pipeline

You can create ML pipelines using the Kubeflow Pipelines SDK:

```python
import kfp
from kfp import dsl

# Define a pipeline
@dsl.pipeline(
    name="Example Pipeline",
    description="A simple example pipeline"
)
def example_pipeline():
    # Define pipeline steps
    data_prep = dsl.ContainerOp(
        name="data-preparation",
        image="your-registry/data-prep:latest",
        command=["python", "process.py"]
    )

    train = dsl.ContainerOp(
        name="model-training",
        image="your-registry/model-train:latest",
        command=["python", "train.py"]
    )

    train.after(data_prep)

# Compile the pipeline
kfp.compiler.Compiler().compile(example_pipeline, "example_pipeline.yaml")

# Upload the pipeline to Kubeflow
client = kfp.Client()
client.upload_pipeline(
    pipeline_package_path="example_pipeline.yaml",
    pipeline_name="Example Pipeline"
)
```

## Monitoring and Logs

You can monitor your AKS cluster and Kubeflow deployment in the Azure Portal:
[Azure Portal](https://portal.azure.com)
