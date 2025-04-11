provider "aws" {
  region = var.region
}

resource "aws_sagemaker_model" "model" {
  name               = var.modelName
  execution_role_arn = var.roleArn

  primary_container {
    image          = var.containerImage
    model_data_url = var.modelDataUrl
  }

  tags = {
    Name        = var.modelName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = "${var.endpointName}-config"

  production_variants {
    variant_name           = "default"
    model_name             = aws_sagemaker_model.model.name
    instance_type          = var.instanceType
    initial_instance_count = var.initialInstanceCount
  }

  tags = {
    Name        = "${var.endpointName}-config"
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "aws_sagemaker_endpoint" "endpoint" {
  name                 = var.endpointName
  endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_config.name

  tags = {
    Name        = var.endpointName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
} 