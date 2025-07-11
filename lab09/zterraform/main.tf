locals {
    project_name = "lol-tracker"    # → LT
}

resource "azurerm_resource_group" "rg" {
    location    = var.resource_group_location
    name        = local.project_name
}

# Create Virtual Network
resource "azurerm_virtual_network" "lt_network" {
    name                = "LT-Vnet"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    address_space       = ["10.0.0.0/16"]
}

# Create Subnet
resource "azurerm_subnet" "lt_subnet" {
    name                    = "LT-Subnet"
    resource_group_name     = azurerm_resource_group.rg.name
    virtual_network_name    = azurerm_virtual_network.lt_network.name
    address_prefixes        = ["10.0.1.0/24"]
}

# Create Public IPs
resource "azurerm_public_ip" "lt_public_ip" {
    name                    = "LT-PUblicIP"
    resource_group_name     = azurerm_resource_group.rg.name
    location                = azurerm_resource_group.rg.location
    allocation_method       = "Dynamic"
    domain_name_label       = var.dns_name
}

# Create Network Security Group and Rule
resource "azurerm_network_security_group" "lt_nsg" {
    name                    = "LT-NetworkSecurityGroup"
    resource_group_name     = azurerm_resource_group.rg.name
    location                = azurerm_resource_group.rg.location

    security_rule {
        name                        = "SSH"
        priority                    = 1001
        direction                   = "Inbound"
        access                      = "Allow"
        protocol                    = "Tcp"
        source_port_range           = "*"
        destination_port_range      = "22"
        source_address_prefix       = "*"
        destination_address_prefix  = "*"
    }

    security_rule {
        name                        = "RECEIVER"
        priority                    = 1002
        direction                   = "Inbound"
        access                      = "Allow"
        protocol                    = "Tcp"
        source_port_range           = "*"
        destination_port_range      = "8080"
        source_address_prefix       = "*"
        destination_address_prefix  = "*"
    }

    security_rule {
        name                        = "PROCESSING"
        priority                    = 1003
        direction                   = "Inbound"
        access                      = "Allow"
        protocol                    = "Tcp"
        source_port_range           = "*"
        destination_port_range      = "8100"
        source_address_prefix       = "*"
        destination_address_prefix  = "*"
    }

    security_rule {
        name                        = "ANALYZER"
        priority                    = 1004
        direction                   = "Inbound"
        access                      = "Allow"
        protocol                    = "Tcp"
        source_port_range           = "*"
        destination_port_range      = "8110"
        source_address_prefix       = "*"
        destination_address_prefix  = "*"
    }
}

# Create Network Interface
resource "azurerm_network_interface" "lt_nic" {
    name                    = "LT-NIC"
    location                = azurerm_resource_group.rg.location
    resource_group_name     = azurerm_resource_group.rg.name

    ip_configuration {
        name                            = "lt_nic_configuration"
        subnet_id                       = azurerm_subnet.lt_subnet.id
        private_ip_address_allocation   = "Dynamic"
        public_ip_address_id            = azurerm_public_ip.lt_public_ip.id
    }
}

# Connect the Security Group to the Network Interface
resource "azurerm_network_interface_security_group_association" "any_name" {
    network_interface_id        = azurerm_network_interface.lt_nic.id
    network_security_group_id   = azurerm_network_security_group.lt_nsg.id
}

# Generate Random Text for a Unique Stroage Account Name
resource "random_id" "random_id" {
    keepers = {
        resource_group = azurerm_resource_group.rg.name
    }
    byte_length = 9
}

# Create Storage Account for Boot Diagnostics
resource "azurerm_storage_account" "lt_storage_account" {
    name                        = "diag${random_id.random_id.hex}"
    resource_group_name         = azurerm_resource_group.rg.name
    location                    = azurerm_resource_group.rg.location
    account_tier                = "Standard"
    account_replication_type    = "LRS"
}

# Create Virtual Machine
resource "azurerm_linux_virtual_machine" "lt_vm" {
    name                    = "LT-VM"
    resource_group_name     = azurerm_resource_group.rg.name
    location                = azurerm_resource_group.rg.location
    network_interface_ids   = [azurerm_network_interface.lt_nic.id]
    size                    = "Standard_DS1_v2"

    os_disk {
        name                    = "LT-OsDisk"
        caching                 = "ReadWrite"
        storage_account_type    = "Premium_LRS"
    }

    source_image_reference {
        publisher   = "Canonical"
        offer       = "0001-com-ubuntu-server-jammy"
        sku         = "22_04-lts-gen2"
        version     = "latest"
    }

    computer_name   = var.username
    admin_username  = var.username

    admin_ssh_key {
        username        = var.username
        public_key      = file(var.public_key)
    }

    boot_diagnostics {
        storage_account_uri = azurerm_storage_account.lt_storage_account.primary_blob_endpoint
    }
}

