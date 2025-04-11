provider "azurerm" {
  features {}
}

provider "helm" {
  kubernetes {
    host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
    client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
    client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
  }
}

resource "azurerm_resource_group" "rg" {
  name     = var.resourceGroupName
  location = var.location
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.clusterName
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = var.clusterName
  kubernetes_version  = var.kubernetesVersion

  default_node_pool {
    name       = "default"
    node_count = var.nodeCount
    vm_size    = var.vmSize
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Name        = var.clusterName
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "helm_release" "kubeflow" {
  name       = "kubeflow"
  repository = "https://github.com/kubeflow/pipelines/releases/download"
  chart      = "kubeflow-pipelines-standalone-${var.kubeflowVersion}"
  version    = var.kubeflowVersion
  namespace  = "kubeflow"
  create_namespace = true

  set {
    name  = "executorImage"
    value = "gcr.io/ml-pipeline/kfp-launcher:${var.kubeflowVersion}"
  }

  depends_on = [
    azurerm_kubernetes_cluster.aks
  ]
} 