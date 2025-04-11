variable "serviceName" {
  description = "Name of the Cloud Run service"
  type        = string
}

variable "description" {
  description = "Description of the Cloud Run service"
  type        = string
  default     = ""
}

variable "projectId" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "image" {
  description = "Container image to deploy"
  type        = string
  default     = "gcr.io/cloudrun/hello"
}

variable "cpu" {
  description = "CPU allocation for the service"
  type        = string
  default     = "1"
}

variable "memory" {
  description = "Memory allocation for the service"
  type        = string
  default     = "256Mi"
}

variable "maxInstances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
} 