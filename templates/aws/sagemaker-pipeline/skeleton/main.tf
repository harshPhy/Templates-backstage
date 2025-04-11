provider "aws" {
  region = var.region
}

locals {
  pipeline_definition = templatefile("${path.module}/pipeline-definitions/${var.pipelineDefinition}.json.tpl", {
    pipeline_name  = var.pipelineName
    role_arn       = var.roleArn
    instance_type  = var.instanceType
    region         = var.region
  })
  
  tags = { for item in var.tags : item.key => item.value }
}

resource "aws_sagemaker_pipeline" "pipeline" {
  pipeline_name         = var.pipelineName
  pipeline_display_name = var.pipelineName
  role_arn              = var.roleArn
  pipeline_description  = var.description
  
  pipeline_definition = local.pipeline_definition

  tags = merge({
    Name        = var.pipelineName
    Description = var.description
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }, local.tags)
} 