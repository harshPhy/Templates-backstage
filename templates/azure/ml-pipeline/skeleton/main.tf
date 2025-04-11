provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ml_rg" {
  name     = "${var.workspaceName}-rg"
  location = var.location
}

resource "azurerm_application_insights" "ml_app_insights" {
  name                = "${var.workspaceName}-ai"
  location            = azurerm_resource_group.ml_rg.location
  resource_group_name = azurerm_resource_group.ml_rg.name
  application_type    = "web"
}

resource "azurerm_key_vault" "ml_kv" {
  name                = "${var.workspaceName}kv"
  location            = azurerm_resource_group.ml_rg.location
  resource_group_name = azurerm_resource_group.ml_rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_storage_account" "ml_storage" {
  name                     = "${replace(var.workspaceName, "-", "")}sa"
  location                 = azurerm_resource_group.ml_rg.location
  resource_group_name      = azurerm_resource_group.ml_rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

data "azurerm_client_config" "current" {}

resource "azurerm_machine_learning_workspace" "ml_workspace" {
  name                    = var.workspaceName
  location                = azurerm_resource_group.ml_rg.location
  resource_group_name     = azurerm_resource_group.ml_rg.name
  application_insights_id = azurerm_application_insights.ml_app_insights.id
  key_vault_id            = azurerm_key_vault.ml_kv.id
  storage_account_id      = azurerm_storage_account.ml_storage.id

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_machine_learning_compute_cluster" "ml_compute" {
  name                          = "${var.workspaceName}-compute"
  location                      = azurerm_resource_group.ml_rg.location
  vm_priority                   = "Dedicated"
  vm_size                       = var.vmSize
  machine_learning_workspace_id = azurerm_machine_learning_workspace.ml_workspace.id
  
  scale_settings {
    min_node_count                    = 0
    max_node_count                    = 4
    scale_down_nodes_after_idle_duration = "PT30M" # 30 minutes
  }

  identity {
    type = "SystemAssigned"
  }
} 