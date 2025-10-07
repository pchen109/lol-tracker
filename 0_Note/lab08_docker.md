
# Lab 08 - Docker (Contanization)

### Purpose
* Containerize all microservices with Docker and deploy with Docker Compose.

### Key Concepts
* Each service has its own `Dockerfile` + `requirements.txt`.
* Use `build` (not prebuilt images) in `docker-compose.yml`.
* Services talk via internal Docker network (no `localhost`).
* Logs, configs, and data mounted in dedicated folders.
* Use `depends_on` and `healthcheck` for startup order.

### Workflow
1. Wrote `requirements.txt` per service with only needed dependencies.
2. Built Dockerfiles (Python base, copy + install reqs, run `app.py`).
3. Updated `docker-compose.yml` to build services, add volumes, set `TZ`.
4. Moved logs → `logs/`, configs → `config/`, data → `data/`.
5. Fixed Kafka host to `kafka` (not localhost).
6. Ran `docker compose up -d --build` to start all services.

# End
