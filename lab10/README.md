# Lab 10 - Dashboard

### Tasks
- Create a Dashboard Service to display stats of Processing and Analysis stats. 
- Deploy the Dabshabord in VM using Ansible

### Results
- The Dashboard displays Processing and Analysis stats
- The Dashboard displays one of each event types randomly
- The Dashboard updates stats periodically or for every 4 seconds

### Prerequisite
##### Azure
1. Create an Azure account and ensure you have an active subscription.
2. Run `az login` in WSL to authenticate.
##### Git Repo
1. Clone this repository.
2. Generate a new **SSH key pair** for Git access using:
   1. `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
3. Add the **public key** (.pub file) to your Git account.
4. Create your own Git repository and push the contents of the `lab10` folder to it.
##### Terraform
1. Generate a new **SSH key pair** for Azure VM access:
   1. `ssh-keygen -t rsa -b 4096 -f ~/.ssh/azure_key`
2. In `terraform.tfvars`, update:
   1. `dns_name` with your unique DNS label.
   2. `public_key` with the path to your public key (e.g., `~/.ssh/azure_key.pub`).
##### Ansible 
1. In `vars.yml`, update:
   1. `repo_url` with your own Git repository URL.
   2. `git_key_loc` to the path of your SSH key.
   3. other variables as needed to match your environment
2. Replace `ansible_host` in `inventory.ini` with your VM's DNS or public IP.

### How to run
1. Clone this repoistory.
2. Open a terminal and navigate to the lab10 project directory:
   1. `cd lab10`
3. Make the deployment script executable (only needed once):
   1. `chmod +x deploy.sh`
4. Run the script to deploy the project:
   1. `./deploy.sh`
5. Enter your DNS name in your browser to display the dashboard

### How to verify Dashboard
1. **SSH** into the VM
   1. `ssh -i <YOUR_PRIVATE_KEY_LOCATION> kekw@<YOUR_DNS>`
2. Verify services are running
   1. `docker compose ps -a`
3. Send test data using **JMeter**
4. **Check if Dashbaord stats has changed**

### How to verify other servieces (Optional)
1. Check **MySQL** container to confirm the received data is correctly stored
2. Verify service stats endpoints
   1. **Receiver** stats: `http://<YOUR_DNS>:8100/stats`
   2. **Analyzer** stats: `http://<YOUR_DNS>:8110/stats`
3. Verify **activity** data
   1. View data at index 0:
      1. `http://<YOUR_DNS>:8110/activity?index=0`
   2. Modify index to inspect different entries
4. Verify **match** data
   1. View data at index 0:
      1. `http://<YOUR_DNS>:8110/match?index=0`
   2. Modify index to inspect different entries 
5.  Inspect logs in the logs/ directory to ensure each service is logging as expected.

### How to Use JMeter for VM
1. Open the **JMeter** application
2. Load the test plan file: `jmeter_vm.jmx` in `~\lab10\zothers` directory
3. In both HTTP Request samplers under VM Group:
   1. Update "**Server Name or IP**" to your own DNS name.
4. Adjust **Number of Threads** and **Loop Count** as desired to simulate different loads.
5. Click the **Start** button (green ▶️) to begin sending events.

### How to Use JMeter for Local (Optional)
*Use this if running `docker compose up -d --build` locally.*
1. Open the **JMeter** application
2. Load the test plan file: `jmeter_local.jmx` in `~\lab10\zothers` directory
3. Adjust **Number of Threads** and **Loop Count** as desired to simulate different loads.
4. Click the **Start** button (green ▶️) to begin sending events.

### How to Check Events in MySQL
1. **SSH** into the VM
   1. `ssh -i <YOUR_PRIVATE_KEY_LOCATION> kekw@<YOUR_DNS>`
2. Access the MySQL container
   1. `docker compose exec db mysql -u riot -priot`
3. Switch to the database
   1. `USE riot;`
4. View user activity events
   1. `SELECT * FROM user_activity;`
5. View user match events
   1. `SELECT * FROM user_match;`

### How to Close
1. run `02_end.sh` in lab10 directory

# End