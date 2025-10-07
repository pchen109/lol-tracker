
# Lab 01 - OpenAPI (Swagger)

### Purpose 
This lab taught me to define REST endpoints with OpenAPI (Swagger)

### Key concepts
* RESTful API vs REST-like (correct use of HTTP verbs).
* OpenAPI spec documents endpoints, schemas, and responses.
* Each event type = its own POST endpoint.
* Events must include ID, numeric property, timestamp, + 1 extra field.

### Workflow summary
1. Defined project's purpose and audience.
2. Defined two events: User Activity + Performance.
3. Created POST endpoints for each event.
4. Defined JSON schemas with required properties.
5. Linked schemas in OpenAPI YAML with components.

### Pseudocode
```python
POST /events/user-activity:
    validate against schema
    if valid: return 201
    else: return 400

POST /events/performance:
    validate against schema
    if valid: return 201
    else: return 400
```
# End