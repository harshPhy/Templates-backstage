output "workspace_name" {
  description = "Name of the Azure ML workspace"
  value       = azurerm_machine_learning_workspace.ml_workspace.name
}

output "workspace_id" {
  description = "ID of the Azure ML workspace"
  value       = azurerm_machine_learning_workspace.ml_workspace.id
}

output "compute_name" {
  description = "Name of the compute cluster"
  value       = azurerm_machine_learning_compute_cluster.ml_compute.name
}

output "workspace_url" {
  description = "URL to access the Azure ML workspace"
  value       = "https://ml.azure.com/workspaces/${azurerm_resource_group.ml_rg.name}/${azurerm_machine_learning_workspace.ml_workspace.name}"
} 