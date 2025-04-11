variable "workspaceName" {
  description = "Name of the Azure ML workspace"
  type        = string
}

variable "pipelineName" {
  description = "Name of the ML pipeline"
  type        = string
}

variable "description" {
  description = "Description of the ML pipeline"
  type        = string
  default     = ""
}

variable "location" {
  description = "Azure region to deploy to"
  type        = string
  default     = "eastus"
}

variable "computeType" {
  description = "Type of compute target to use for the pipeline"
  type        = string
  default     = "amlcompute"
  
  validation {
    condition     = contains(["amlcompute", "kubernetes", "databricks"], var.computeType)
    error_message = "Compute type must be one of: amlcompute, kubernetes, databricks."
  }
}

variable "vmSize" {
  description = "VM size for the compute target"
  type        = string
  default     = "Standard_D2_v2"
} 