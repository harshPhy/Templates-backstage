# ${{values.functionName}}

${{values.description}}

This Terraform configuration creates an AWS Lambda function with the following properties:

- **Function Name**: ${{values.functionName}}
- **Runtime**: ${{values.runtime}}
- **Handler**: ${{values.handler}}
- **Memory Size**: ${{values.memorySize}} MB
- **Timeout**: ${{values.timeout}} seconds

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (v1.0.0 or newer)

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

## Function Code

This template includes a placeholder file for your Lambda function code. You need to create your function code and package it as a ZIP file named `function.zip`.

For Python functions:

```python
def handler(event, context):
    print("Hello from Lambda!")
    return {
        'statusCode': 200,
        'body': 'Success!'
    }
```
