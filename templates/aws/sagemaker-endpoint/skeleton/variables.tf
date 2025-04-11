variable "region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "endpointName" {
  description = "Name of the SageMaker endpoint"
  type        = string
}

variable "modelName" {
  description = "Name of the model to deploy"
  type        = string
}

variable "roleArn" {
  description = "ARN of the IAM role that SageMaker can assume to perform tasks"
  type        = string
}

variable "description" {
  description = "Description of the endpoint"
  type        = string
  default     = ""
}

variable "instanceType" {
  description = "Amazon EC2 instance type for the endpoint"
  type        = string
  default     = "ml.t2.medium"
}

variable "initialInstanceCount" {
  description = "Initial number of instances for the endpoint"
  type        = number
  default     = 1
}

variable "modelDataUrl" {
  description = "S3 URL to the model artifacts"
  type        = string
}

variable "containerImage" {
  description = "URI to the container image for model inference"
  type        = string
  default     = "763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-inference:2.6.3-cpu"
} 