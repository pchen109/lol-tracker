
# Lab 05 - Processing

### Purpose
* Extend Storage with query endpoints (GET with start/end timestamps).
* Create a Processing service that periodically pulls new events, calculates stats, logs activity, and saves results in a JSON file.

### Key Concepts
* Querying by timestamp range in REST API.
* Periodic jobs with APScheduler.
* Logging with external YAML config.
* Persisting stats in JSON file.
* Handling time zones in MySQL.

### Workflow
1. Added GET endpoints in Storage with start/end timestamps.
2. Updated DB and code to handle time zones + timestamp queries.
3. Built Processing service with OpenAPI spec + `apscheduler`.
4. Configured Processing to read/write JSON stats + use external config.
5. Ran Receiver → Storage → Processing, then send test events.
6. Verify JSON stats update + check log files.

```sql
every N seconds:
    read last_updated from data.json
    request new events from Storage(start, end)
    if response OK:
        update cumulative stats
        write stats + new last_updated to data.json
    log success or error
```
# End

