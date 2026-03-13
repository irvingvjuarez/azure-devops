terraform {
  backend "azurerm" {
    storage_account_name = "ivjdevops"
    container_name       = "tfstate"
    key                  = "devops.tfstate"
  }
}
