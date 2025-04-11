variable "resourceGroupName" {
  description = "Name of the Azure resource group"
  type        = string
}

variable "functionAppName" {
  description = "Name of the Azure Function App"
  type        = string
}

variable "location" {
  description = "Azure region to deploy to"
  type        = string
  default     = "eastus"
}

variable "runtime" {
  description = "Runtime to use for the function app"
  type        = string
  default     = "python"
  validation {
    condition     = contains(["python", "node", "dotnet", "java"], var.runtime)
    error_message = "Runtime must be one of: python, node, dotnet, java."
  }
}

variable "runtimeVersion" {
  description = "Version of the runtime"
  type        = string
  default     = "3.9"
}

variable "storageSku" {
  description = "SKU for the storage account"
  type        = string
  default     = "LRS"
}

variable "tier" {
  description = "Tier for the App Service Plan"
  type        = string
  default     = "Dynamic"
  validation {
    condition     = contains(["Dynamic", "Basic", "Standard", "Premium"], var.tier)
    error_message = "Tier must be one of: Dynamic, Basic, Standard, Premium."
  }
}

variable "size" {
  description = "Size for the App Service Plan"
  type        = string
  default     = "Y1"
} 