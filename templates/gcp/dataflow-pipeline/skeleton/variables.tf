variable "projectId" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "jobName" {
  description = "Name of the Dataflow job"
  type        = string
}

variable "region" {
  description = "GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "templatePath" {
  description = "GCS path to the Dataflow template"
  type        = string
}

variable "tempLocation" {
  description = "GCS path for temporary files"
  type        = string
}

variable "serviceAccount" {
  description = "Service account to run the Dataflow job"
  type        = string
  default     = ""
}

variable "machineType" {
  description = "Machine type for Dataflow workers"
  type        = string
  default     = "n1-standard-2"
}

variable "maxWorkers" {
  description = "Maximum number of workers"
  type        = number
  default     = 5
}

variable "network" {
  description = "VPC network to use for the Dataflow job"
  type        = string
  default     = ""
}

variable "subnetwork" {
  description = "Subnetwork to use for the Dataflow job"
  type        = string
  default     = ""
} 