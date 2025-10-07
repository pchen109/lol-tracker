
# Lab 02 - Receiver

### Purpose 
This lab taught me to build a Receiver Service that handles multiple event types, stores them in a JSON file, and validates incoming requests using OpenAPI (Swagger). It also introduced basic load testing with Postman and JMeter.

### Key Concepts
* Connexion framework = OpenAPI (openapi.yml) + Python (app.py).
* Event data logging to a JSON file with constraints (max 5 recent events per type).
* Strict request and response validation in OpenAPI.
* Handling race conditions when writing to a file (thread.Lock()).
* Load testing and concurrency simulation using Apache JMeter.

### Workflow Summary
1. Created Receiver service with connexion and link OpenAPI YAML.
2. Implemented API endpoint functions to print and store payloads in events.json.
3. Enabled strict validation and ensure invalid requests are rejected.
4. Tested endpoints individually with Swagger UI / Postman and simulate concurrency with JMeter.

### Pseudocode
```python
# Endpoint for Event Type 1
def receive_event_type1(body):
    validate body against schema
    acquire file lock
    load events.json
    update recent events (max 5)
    save events.json
    release lock
    return 201 or 400

# Endpoint for Event Type 2
def receive_event_type2(body):
    validate body against schema
    acquire file lock
    load events.json
    update recent events (max 5)
    save events.json
    release lock
    return 201 or 400
```

# End