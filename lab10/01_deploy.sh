#!/bin/bash

# Step 1: Provision Infrastruture
cd ./zterraform
terraform init
terraform apply --auto-approve

# # Step 2: Extract Public IP
# IP=$(terraform output -raw public_ip_address)

# Step 3: Run Ansible with the IP
sleep 10            # wait till virtual machine is ready
cd ../zansible
ansible-playbook -i inventory.ini \
    playbook.yml