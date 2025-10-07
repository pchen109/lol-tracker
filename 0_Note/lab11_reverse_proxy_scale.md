
# Lab 11 – Reverse Proxy and Scale

### Purpose
* Introduce a single endpoint for all services using **NGINX as a reverse proxy**.
* Scale services (Receiver, Storage) with Docker to handle increased load.

### Key Concepts
* **Reverse Proxy (NGINX)**: routes client requests to internal services.
  * `/` → Dashboard UI
  * `/processing` → Processing service
  * `/analyzer` → Analyzer service
* **Service Base Path**: update each service’s `base_path` to match NGINX routing.
* **Internal Docker Network**: only NGINX is exposed to the public; all other services are internal.
* **Scaling**: use Docker Compose `--scale` or `deploy.replicas` to run multiple instances of Receiver.
* **CORS**: no longer needed because requests go through the proxy.

### Workflow
1. Copy and update `nginx.conf` to map endpoints to services.
2. Update `base_path` in each service (`app.py`) to match NGINX routing.
3. Disable CORS in service configs.
4. Update Dockerfile / Compose to use custom `nginx.conf`.
5. Deploy all services to VM with Ansible (`./deploy.sh`).
6. Verify services via browser (Dashboard) and JMeter load tests.
7. Scale Receiver and confirm multiple containers running (`docker compose ps`).

### Verification
* Dashboard accessible at `http://<VM_DNS>/`.
* Requests properly routed to `/processing` and `/analyzer`.
* JMeter confirms load balancing works for scaled services.
* MySQL contains correct activity and match data.
* Only NGINX service exposed to public; other services remain internal.

# End