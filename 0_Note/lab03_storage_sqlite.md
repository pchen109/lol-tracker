
# Lab 03 - Stoarage

### Purpose
* Build a **Storage service** to persist events in a database.
* Integrate **Receiver** with **Storage** (Receiver forwards, Storage saves).
* Use **JMeter** to send random, high-volume events.

### Key Concepts
* **Database per Service** → each microservice manages its own DB.
* **SQLite + SQLAlchemy ORM** for lightweight relational storage.
* **Receiver → Storage → DB** integration via HTTP (using `httpx`).
* **Race conditions** possible in SQLite (only one writer at a time).
* **JMeter** random variables simulate varied load testing.

### Workflow
1. Created Storage `app.py` with SQLite + SQLAlchemy models.
2. Defined DB init, models, and management scripts.
3. Modified Storage `app.py` to insert events into DB.
4. Updated Receiver to forward POST requests to Storage (port 8090).
5. Use Swagger to test endpoints → verify data in DB.
6. Run JMeter with random values to test under load.

### Pseudocode
```python
# Receiver
def receive_event(body):
    r = httpx.post("http://localhost:8090/event", json=body)
    return NoContent, r.status_code

# Storage
def store_event(body):
    session = make_session()
    event = EventModel(**body)
    session.add(event)
    session.commit()
    session.close()
    return NoContent, 201
```

# End