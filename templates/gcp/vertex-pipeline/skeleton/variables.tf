variable "projectId" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "pipelineName" {
  description = "Name of the Vertex AI pipeline"
  type        = string
}

variable "region" {
  description = "GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "description" {
  description = "Description of the pipeline"
  type        = string
  default     = ""
}

variable "pipelineSpecPath" {
  description = "Path to the pipeline specification file"
  type        = string
}

variable "serviceAccount" {
  description = "Service account to run the pipeline"
  type        = string
  default     = ""
}

variable "machineType" {
  description = "Machine type for pipeline components"
  type        = string
  default     = "n1-standard-4"
}

variable "network" {
  description = "VPC network to use for the pipeline"
  type        = string
  default     = ""
} 