variable "resourceGroupName" {
  description = "Name of the Azure resource group"
  type        = string
}

variable "clusterName" {
  description = "Name of the Azure Kubernetes Service cluster"
  type        = string
}

variable "location" {
  description = "Azure region to deploy to"
  type        = string
  default     = "eastus"
}

variable "kubernetesVersion" {
  description = "Version of Kubernetes to use"
  type        = string
  default     = "1.25.5"
}

variable "vmSize" {
  description = "Size of the VM for AKS nodes"
  type        = string
  default     = "Standard_D4s_v3"
}

variable "nodeCount" {
  description = "Number of nodes in the AKS cluster"
  type        = number
  default     = 3
}

variable "kubeflowVersion" {
  description = "Version of Kubeflow to deploy"
  type        = string
  default     = "1.7.0"
} 