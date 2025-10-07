
# Lab 07 - Analyzer

### Purpose
* Created a new **Analyzer** service that consumes Kafka messages and exposes GET endpoints for querying event history and stats.

### Key Concepts
* Kafka queue stores *both* event types in a single topic → Analyzer needs to track separate indexes for each.
* Analyzer endpoints:

  * `/activity?index=n` → get user activity at index `n`
  * `/match?index=n` → get user match at index `n`
  * `/stats` → return count of each event type
* Externalized config (`app_conf.yml`) for Kafka connection + logging.
* Uses `pykafka` `SimpleConsumer` with offsets and timeouts.

### Workflow

1. Built **Analyzer** service with OpenAPI YAML (3 GET endpoints).
2. Installed `pykafka`, configured Analyzer to connect to Kafka.
3. Wrote consumer code to scan Kafka messages and return requested index.
4. Added `/stats` endpoint to count `user_activity` + `user_match`.
5. Externalized configs for Kafka + logging.
6. Tested via Swagger (`/activity`, `/match`, `/stats`) + JMeter + logs.

### Pseudocode (for index lookup)
```
function get_event(event_type, index):
    connect to Kafka topic
    counter = 0
    for each msg in consumer:
        if msg.type == event_type:
            if counter == index:
                return msg.payload
            counter += 1
    return "Not found", 404
```
# End
