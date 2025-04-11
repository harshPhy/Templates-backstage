variable "projectId" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "clusterName" {
  description = "Name of the Google Kubernetes Engine cluster"
  type        = string
}

variable "region" {
  description = "GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone to deploy to"
  type        = string
  default     = "us-central1-a"
}

variable "kubernetesVersion" {
  description = "Version of Kubernetes to use"
  type        = string
  default     = "1.24"
}

variable "machineType" {
  description = "Machine type for GKE nodes"
  type        = string
  default     = "e2-standard-4"
}

variable "nodeCount" {
  description = "Number of nodes in the GKE cluster"
  type        = number
  default     = 3
}

variable "kubeflowVersion" {
  description = "Version of Kubeflow to deploy"
  type        = string
  default     = "1.7.0"
} 