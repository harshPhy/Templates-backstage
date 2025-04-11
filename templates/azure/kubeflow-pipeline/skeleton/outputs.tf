output "cluster_name" {
  description = "Name of the AKS cluster"
  value       = azurerm_kubernetes_cluster.aks.name
}

output "cluster_id" {
  description = "ID of the AKS cluster"
  value       = azurerm_kubernetes_cluster.aks.id
}

output "kube_config_raw" {
  description = "Raw Kubernetes config for connecting to the cluster"
  value       = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive   = true
}

output "host" {
  description = "Kubernetes cluster host"
  value       = azurerm_kubernetes_cluster.aks.kube_config.0.host
  sensitive   = true
}

output "kubeflow_ui_endpoint" {
  description = "Endpoint for accessing Kubeflow UI"
  value       = "http://${azurerm_kubernetes_cluster.aks.fqdn}:8080"
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.rg.name
}

output "azure_portal_url" {
  description = "URL to view the AKS cluster in the Azure Portal"
  value       = "https://portal.azure.com/#resource/subscriptions/"
}