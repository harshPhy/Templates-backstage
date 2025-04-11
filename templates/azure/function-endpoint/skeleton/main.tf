provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "function_rg" {
  name     = var.resourceGroupName
  location = var.location
}

resource "azurerm_storage_account" "function_storage" {
  name                     = "${replace(lower(var.functionAppName), "-", "")}sa"
  resource_group_name      = azurerm_resource_group.function_rg.name
  location                 = azurerm_resource_group.function_rg.location
  account_tier             = "Standard"
  account_replication_type = var.storageSku

  tags = {
    Name        = "${var.functionAppName}-storage"
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
}

resource "azurerm_service_plan" "function_plan" {
  name                = "${var.functionAppName}-plan"
  location            = azurerm_resource_group.function_rg.location
  resource_group_name = azurerm_resource_group.function_rg.name
  os_type             = "Linux"
  sku_name            = var.tier == "Dynamic" ? "Y1" : var.size
}

resource "azurerm_application_insights" "function_insights" {
  name                = "${var.functionAppName}-insights"
  location            = azurerm_resource_group.function_rg.location
  resource_group_name = azurerm_resource_group.function_rg.name
  application_type    = "web"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = var.functionAppName
  location            = azurerm_resource_group.function_rg.location
  resource_group_name = azurerm_resource_group.function_rg.name
  service_plan_id     = azurerm_service_plan.function_plan.id
  
  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key

  site_config {
    application_stack {
      dynamic "python" {
        for_each = var.runtime == "python" ? [1] : []
        content {
          version = var.runtimeVersion
        }
      }

      dynamic "node" {
        for_each = var.runtime == "node" ? [1] : []
        content {
          version = var.runtimeVersion
        }
      }

      dynamic "dotnet" {
        for_each = var.runtime == "dotnet" ? [1] : []
        content {
          version = var.runtimeVersion
        }
      }

      dynamic "java" {
        for_each = var.runtime == "java" ? [1] : []
        content {
          version = var.runtimeVersion
        }
      }
    }
  }

  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.function_insights.instrumentation_key
    "FUNCTIONS_WORKER_RUNTIME"       = var.runtime
    "AzureWebJobsStorage"            = azurerm_storage_account.function_storage.primary_connection_string
  }

  tags = {
    Name        = var.functionAppName
    ManagedBy   = "Terraform"
    Source      = "Backstage Template"
  }
} 