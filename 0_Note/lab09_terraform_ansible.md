
# Lab 09 – Terrafrom and Ansible (Deployment)

### Purpose
* Automate deployment of microservices project to a cloud VM.
* Use Git for version control and Ansible/Terraform for provisioning + deployment.

### Key Concepts
* **Terraform**: provision Azure VM (Ubuntu + Docker + Docker Compose).
* **Git**: manage codebase, ignore prod configs/logs/data, use deploy keys for VM access.
* **Ansible**: automate install, folder setup, Git pull, and service deployment.
* Separate **dev vs prod configs** → dev in repo, prod ignored.
* Services run via `docker compose` on VM and exposed with DNS/public IP.

### Workflow
1. Provision VM with Terraform (DNS, SSH, Docker installed).
2. Set up Git repo (ignore logs/data, add deploy key for VM).
3. Configure Ansible (`inventory.ini`, `vars.yml`) with repo URL, SSH key, host.
4. Run `./deploy.sh` → Ansible installs packages, clones repo, runs `docker compose up -d`.
5. Verify deployment by:

   * Checking running containers (`docker compose ps -a`).
   * Sending test events via JMeter.
   * Inspecting data in MySQL (`SELECT * FROM user_activity;`).
   * Checking `/stats`, `/activity`, `/match` endpoints on Analyzer + Receiver.
6. Tear down with `02_end.sh`.

# End