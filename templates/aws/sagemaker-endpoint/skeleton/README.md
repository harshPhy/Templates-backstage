# AWS SageMaker Endpoint: ${{values.endpointName}}

${{values.description}}

This Terraform configuration creates an AWS SageMaker endpoint for model serving with the following properties:

- **Endpoint Name**: ${{values.endpointName}}
- **Model Name**: ${{values.modelName}}
- **Instance Type**: ${{values.instanceType}}
- **Initial Instance Count**: ${{values.initialInstanceCount}}

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)
- IAM role with appropriate permissions for SageMaker
- Model artifacts stored in S3
- Container image for inference

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

## Invoking the Endpoint

Once deployed, you can invoke the endpoint using the AWS CLI:

```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name ${{values.endpointName}} \
  --content-type application/json \
  --body '{"instances": [...]}' \
  output.json
```

Or using the AWS SDK in your preferred programming language:

```python
import boto3

runtime = boto3.client('sagemaker-runtime')
response = runtime.invoke_endpoint(
    EndpointName='${{values.endpointName}}',
    ContentType='application/json',
    Body='{"instances": [...]}'
)

result = response['Body'].read().decode()
print(result)
```

## Monitoring

You can monitor your endpoint's performance metrics and logs in the SageMaker console:
[SageMaker Endpoints Console](https://console.aws.amazon.com/sagemaker/home#/endpoints)
