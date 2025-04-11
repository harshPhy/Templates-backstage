# GCP Kubeflow Pipeline on GKE: ${{values.clusterName}}

This Terraform configuration deploys Kubeflow Pipelines on Google Kubernetes Engine (GKE) with the following properties:

- **Project ID**: ${{values.projectId}}
- **Cluster Name**: ${{values.clusterName}}
- **Region**: ${{values.region}}
- **Zone**: ${{values.zone}}
- **Kubernetes Version**: ${{values.kubernetesVersion}}
- **Machine Type**: ${{values.machineType}}
- **Node Count**: ${{values.nodeCount}}
- **Kubeflow Version**: ${{values.kubeflowVersion}}

## Prerequisites

- Google Cloud SDK installed and configured
- Terraform installed (v1.0.0 or newer)
- kubectl installed
- Google Cloud Project with billing enabled
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

## Connecting to the Cluster

After the deployment is complete, you can connect to the cluster using kubectl:

```bash
gcloud container clusters get-credentials ${{values.clusterName}} --zone ${{values.zone}} --project ${{values.projectId}}
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
        image="gcr.io/your-project/data-prep:latest",
        command=["python", "process.py"]
    )

    train = dsl.ContainerOp(
        name="model-training",
        image="gcr.io/your-project/model-train:latest",
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

## Running a Pipeline

Once you've created a pipeline, you can run it:

```python
experiment = client.create_experiment("my-experiment")
run = client.run_pipeline(
    experiment_id=experiment.id,
    job_name="my-pipeline-run",
    pipeline_id="Example Pipeline"
)
```

## Monitoring and Logs

- Monitor your GKE cluster: [GKE Console](https://console.cloud.google.com/kubernetes)
- Monitor your Kubeflow pipelines: Kubeflow Pipelines UI
- View logs: [Cloud Logging](https://console.cloud.google.com/logs)
