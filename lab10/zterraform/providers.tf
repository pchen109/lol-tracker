# set up TF version requirements and provider dependencies
terraform {
    required_version = ">=0.12"

    required_providers {
        # TF provider developed by Microsoft 
        azapi = {
            source = "azure/azapi"
            version = "~>1.5"
        }

        # Azure Resource Manager provider from HashiCorp
        azurerm = {
            source = "hashicorp/azurerm"
            version = "~>3.0"
        }
        # Random provider
        random = {
            source = "hashicorp/random"
            version = "~>3.0"
        }
    }
}

# declare and configure the Azure provider for use
provider "azurerm" {
    features {}
}