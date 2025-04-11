output "function_app_name" {
  description = "Name of the Azure Function App"
  value       = azurerm_linux_function_app.function_app.name
}

output "function_app_id" {
  description = "ID of the Azure Function App"
  value       = azurerm_linux_function_app.function_app.id
}

output "function_app_default_hostname" {
  description = "Default hostname of the Azure Function App"
  value       = azurerm_linux_function_app.function_app.default_hostname
}

output "function_app_endpoint" {
  description = "Endpoint URL of the Azure Function App"
  value       = "https://${azurerm_linux_function_app.function_app.default_hostname}"
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.function_rg.name
}

output "storage_account_name" {
  description = "Name of the storage account"
  value       = azurerm_storage_account.function_storage.name
}

output "app_insights_instrumentation_key" {
  description = "Instrumentation key for Application Insights"
  value       = azurerm_application_insights.function_insights.instrumentation_key
  sensitive   = true
}

output "azure_portal_url" {
  description = "URL to view the Function App in the Azure Portal"
  value       = "https://portal.azure.com/#@/resource${azurerm_linux_function_app.function_app.id}"
} 