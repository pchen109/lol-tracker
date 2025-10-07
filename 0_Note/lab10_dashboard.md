
# Lab 10 – Dashboard

### Purpose
* Build and deploy a Dashboard UI to visualize Processing + Analyzer stats.
* Run the Dashboard as a Docker container and deploy to VM with Ansible.

### Key Concepts
* SPA (Single Page App) built with plain HTML/JS (“Vanilla JS”).
* Calls `/stats` endpoints (Processing + Analyzer) every 2–4s.
* Displays system logo + random sample event from each type.
* Requires disabling CORS in backend (Processing + Analyzer).
* Runs inside an `nginx` Docker image.

### Workflow
1. Created Dashboard UI with Vanilla JS → call `/stats` + display events.
2. Configured Dockerfile (`FROM nginx … COPY . /usr/share/nginx/html`).
3. Enabled CORS in backend services (Processing + Analyzer).
4. Deployed service to VM using Ansible (`./deploy.sh`).
5. Verified via browser (VM DNS), JMeter load test, and DB queries.

# End
