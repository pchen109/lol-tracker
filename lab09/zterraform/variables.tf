variable "resource_group_location" {
    type            = string 
    default         = "eastus"
    description     = "Location of the resource group"
}

variable "resource_group_name_prefix" {
    type            = string
    default         = "rg"
    description     = "Prefix of the resource group name"
}

variable "username" {
    type            = string
    default         = "kekw"
    description     = "The username for the local account"
}

variable "dns_name"{
    type            = string
    description     = "The DNS name for the VM"
}

variable "public_key" {
    type            = string
    description     = "File path of the public key"
}