
# Lab 04 - MySQL, Logging & Config

### Purpose
* Switch from **SQLite → MySQL** for better scalability.
* Add **external configuration** to avoid hardcoding.
* Add **logging** to track and trace events with `trace_id`.


### Key Concepts
* **Dockerized MySQL** → portable database setup.
* **Config files (YAML)** → flexible, hide credentials.
* **Logging config (YAML)** → log to console + file (`app.log`).
* **Trace ID** → link request/response across services.
* **Service integration** → Receiver forwards, Storage inserts into MySQL.

### Workflow
1. Created MySQL container with docker compose.
2. Updated Storage DB engine to `mysql+pymysql://...`.
3. Added `trace_id` to events (UUID or timestamp).
4. Created app_conf.yml files for Receiver (event URLs) and Storage (DB credentials).
5. Created log_conf.yml and configure logging for console + app.log.
6. Modified Receiver and Storage code to load config and write logs.
7. Sent test events via Swagger → verify in MySQL.
8. Ran JMeter with random events → check logs + DB inserts.

### Pseudocode
```python
# Receiver
trace_id = str(uuid.uuid4())
logger.info(f"RECEIVED event (trace_id={trace_id})")

r = httpx.post(storage_url, json={**body, "trace_id": trace_id})
logger.info(f"RESPONSE (trace_id={trace_id}) status={r.status_code}")

# Storage
def store_event(body):
    session = make_session()
    event = EventModel(**body)
    session.add(event)
    session.commit()
    logger.debug(f"SUCCESS store event (trace_id={body['trace_id']})")
    session.close()
    return NoContent, 201
```
# End
