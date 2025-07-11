# Lab9 - Deployment

##### Purpose 
- Automate the deployment process to a cloud VM
- Use git to manage and version source code

##### Part 1 - Cloud VM
- choose a cloud provider such as Azure or AWS
- choose a recent Linux distribution (i.e., `Ubuntu 24.04`)
- make sure you have a SSH key to SSH access
- use Terraform to create a VM instance
- make sure you have a DNS name for the VM
- make sure Docker and Docker Compose are installed on the VM

##### Part 2 - Git Repo
###### Local Repo
- easier to have a single repo for our labs
- use `git init` to set up the local repo
- add `logs` and `data` in `.gitignore`
- separate config files for development and production environment
	- development env is local	→ dev config can go to Git
	- production env is VM		→ prod config CANNOT go to Git
		- add prod config in `.gitignore`
- use this [default .ignore](https://github.com/github/gitignore/blob/main/Python.gitignore) as a template or starting point
- add all source files and commit to the local repo

###### Remote Repo
- create a git repo on GitHub or any other Git platform
- (optional) make your repo private
- set it up with SSH for pull/push
- use [**Deploy Key**](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys#deploy-keys) to pull/push from the VM

##### Part 3 - Deployment Automation
- use Ansible to install software and deploy tasks 
- do NOT use relative path → able to run from any location
- cover all edge cases
	- missing volumes
	- missing folders
	- missing files
- update the code on the server from Git with Ansible
- verify deployment result with JMeter

##### Ansible Modules
- [GIT Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html)
- [Package Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_module.html#ansible-collections-ansible-builtin-package-module)
- [File Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html#ansible-collections-ansible-builtin-file-module)
- [Copy Module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html#ansible-collections-ansible-builtin-copy-module)

##### Terraform & Azure Documents
- [Terraform Installation - Linux/Ubuntu](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

##### Commands
- **Azure CLI Setup**
	- `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
	- `az version`
	- `az login`
	- `az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/<subscription-id>"`
		- Output:
			- `appId`				- ARM Client ID
			- `displayName`		
			- `password`			- ARM Client Secret
			- `tenant`			- ARM Tenant ID
		- Note:
			- ARM Subscription ID is the Azure Sub ID
	- `nano ~/.bashrc`
		```c
		export ARM_CLIENT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
		export ARM_CLIENT_SECRET="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
		export ARM_SUBSCRIPTION_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
		export ARM_TENANT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
		```
	- `source ~/.bashrc`
- **SSH Key Pair**
	- `ssh-keygen -t rsa -b 4096 -f ~/.ssh/azure_key`
		- Generates a 4096-bit RSA key pair. (GPT)

##### Common AzureRM Env Variable TF
| Env Variable          | Used for                    |
| --------------------- | --------------------------- |
| `ARM_CLIENT_ID`       | Service Principal Client ID |
| `ARM_CLIENT_SECRET`   | Service Principal Secret    |
| `ARM_SUBSCRIPTION_ID` | Azure Subscription ID       |
| `ARM_TENANT_ID`       | Azure Tenant ID             |
##### AZ commands differences (GPT)
- `az account show`
- `az logout`
- `az login`

| Command             | Origin                                      | Purpose                             | Notes                                                                              |
| ------------------- | ------------------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------- |
| `Connect-AzAccount` | PowerShell (`Az` module)                    | Signs in to Azure (creates session) | **Preferred**, replaces `Login-AzAccount`; standardized verb ("Connect")           |
| `Login-AzAccount`   | PowerShell (older `AzureRM` and early `Az`) | Signs in to Azure                   | **Legacy**, deprecated — alias to `Connect-AzAccount` now                          |
| `az login`          | Azure CLI (`az` command-line tool)          | Signs in to Azure                   | CLI-based (not PowerShell), works cross-platform, outputs tokens usable in scripts |
##### Storage Account - AWS vs Azure (GPT)
- **AWS** = More flexible (CloudWatch optional, basic logs always available).    
- **Azure** = More rigid (must pre-configure storage for full diagnostics).

##### Network Architecture - (DeepSeek)
1. **Public IP** must attach to the **NIC**, not the VM directly.
2. **NSG** can apply to _either_ NIC (single VM) or Subnet (all VMs in it).
3. **Storage Account** is standalone but linked to the VM for logs/disks.
```
Storage Account (optional, for diagnostics/disks)
│
VM
│
└── NIC 
    ├── Private IP (from Subnet)
    ├── Public IP (optional)
    └── NSG (firewall rules)
        │
Subnet → VNet
```

##### Knowledge
- warning message: "using the discovered Python interpreter"
	- ansible: `inventory.ini`
	```YAML
	[all]
	kekw-vm ansible_python_interpreter=/usr/bin/python3.10
	```
- Clone Git repo from a specific folder
	```bash
	git clone git@github.com:whatever folder-name
	```
- Specify host alternative name with multiple key pairs
	- `~/.ssh/config`
		```SSH
		Host github.com_lol_tracker
			HostName github.com
			User git
			IdentityFile ~/.ssh/github_lol_tracker
			IdentitiesOnly yes
		```
	- → `git clone github.com_lol_tracker:pchen109/lol_tracker.git lab9`
- Dynamic Inventory 
	- Azure has too many issues →→→ Don't even use it
	- **AWS**: Region is a top-level organizational concept; there's no mandatory grouping of EC2 instances.
		```yaml
		plugin: amazon.aws.aws_ec2
		regions:
		  - us-west-2
		compose:
		  ansible_host: public_dns_name
		hostnames:
		  - name: tag:Name
		    separator: ""
		    prefix: ""
		keyed_groups:
		  - key: tags.group
		    prefix: "group"
		    separator: "_"
		  - key: tags.Project
		    prefix: "project"
		    separator: "_"
		  - key: tags.Role
		    prefix: "server_role"
		    separator: "_"
		```
- Ansible → `inventory.ini`
	- `[azure_vms]` 	→ host group
	- `[all]`			→ all host groups
	- `kekw-vm`		→ a host alias
	```yaml
	[azure_vms]
	kekw-vm ansible_host=40.87.71.27 ansible_user=azure_vms ansible_ssh_private_key_file=~/.ssh/azure_key
	
	# Explicitly specify the Python interpreter version to avoid using the system default
	[all]
	kekw-vm ansible_python_interpreter=/usr/bin/python3.10
	```
- Playbook snippet 
	- `hosts` can be either `azure_vms` or `kekw-vm`
		- `azure_vms`	→ all hosts in this group
		- `kekw-vm`		→ only this host
		```yaml
		- name: Deplloy LOL Tracker
		  hosts: kekw-vm
		  become: true
		```
- GIT URL Setup
	- `git remote -v`
	- `git remote set-url origin git@github.com_lol_tracker:pchen109/lol-tracker.git`
# End
