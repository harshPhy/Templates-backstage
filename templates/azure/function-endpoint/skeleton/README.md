# Azure Function Endpoint: ${{values.functionAppName}}

This Terraform configuration creates an Azure Function App for serverless model serving with the following properties:

- **Function App Name**: ${{values.functionAppName}}
- **Resource Group**: ${{values.resourceGroupName}}
- **Location**: ${{values.location}}
- **Runtime**: ${{values.runtime}}
- **Runtime Version**: ${{values.runtimeVersion}}
- **Tier**: ${{values.tier}}

## Prerequisites

- Azure CLI installed and configured with appropriate credentials
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

## Adding Your Function Code

After deploying the infrastructure, you can add your function code using one of the following methods:

### 1. Azure Functions Core Tools

```bash
# Navigate to your function code directory
cd your-function-code

# Log in to Azure
az login

# Deploy your function code
func azure functionapp publish ${{values.functionAppName}}
```

### 2. CI/CD Pipeline

Configure a CI/CD pipeline in Azure DevOps or GitHub Actions to deploy your function code.

### 3. Zip Deployment

```bash
# Create a zip file with your function code
zip -r function.zip .

# Deploy the zip file to your function app
az functionapp deployment source config-zip -g ${{values.resourceGroupName}} -n ${{values.functionAppName}} --src function.zip
```

## Sample Function Code for ML Model Serving

Here's a simple example of a Python function for model serving:

```python
import azure.functions as func
import json
import numpy as np
from joblib import load

# Load your model (in a real scenario, consider loading once and caching)
model = load('model.joblib')

app = func.FunctionApp()

@app.route(route="predict")
def predict(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get the request body
        req_body = req.get_json()

        # Parse input features
        features = np.array(req_body['features']).reshape(1, -1)

        # Make a prediction
        prediction = model.predict(features).tolist()

        # Return the prediction
        return func.HttpResponse(
            json.dumps({"prediction": prediction}),
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )
```

## Monitoring and Logs

You can monitor your function app's performance and logs in the Azure Portal:
[Azure Portal](https://portal.azure.com)
