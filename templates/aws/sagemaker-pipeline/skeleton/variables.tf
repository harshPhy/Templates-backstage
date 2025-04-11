variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "pipelineName" {
  description = "Name of the SageMaker pipeline"
  type        = string
}

variable "description" {
  description = "Description of the pipeline"
  type        = string
  default     = ""
}

variable "roleArn" {
  description = "ARN of the IAM role that SageMaker can assume to perform tasks"
  type        = string
}

variable "pipelineDefinition" {
  description = "Type of pipeline definition"
  type        = string
  default     = "training"
  validation {
    condition     = contains(["training", "processing", "inference", "custom"], var.pipelineDefinition)
    error_message = "Pipeline definition must be one of: training, processing, inference, custom."
  }
}

variable "instanceType" {
  description = "Amazon EC2 instance type for training/processing jobs"
  type        = string
  default     = "ml.m5.large"
}

variable "tags" {
  description = "Tags to apply to the pipeline"
  type = list(object({
    key   = string
    value = string
  }))
  default = []
} 