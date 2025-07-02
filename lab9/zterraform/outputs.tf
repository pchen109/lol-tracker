output "resource_group_name" {
    value = azurerm_resource_group.rg.name
}

output "public_ip_address" {
    value = azurerm_linux_virtual_machine.lt_vm.public_ip_address
}

output "public_DNS" {
    value = azurerm_public_ip.lt_public_ip.fqdn
}