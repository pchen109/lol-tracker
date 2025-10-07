
# Lab 06 - Kafka and Zookeeper

### Purpose
* Use **Kafka** + **ZooKeeper** as an async message system.
* Receiver produces events → Kafka.
* Storage consumes events from Kafka and saves to MySQL.

### Key Concepts
* Kafka = event queue (decouples Receiver & Storage).
* ZooKeeper = coordinates Kafka cluster.
* Producer (Receiver) vs Consumer (Storage).
* Consumer offset → prevents reprocessing old messages.

### Workflow
1. Created Kafka + ZooKeeper with Docker Compose yml.
2. Receiver sends messages to Kafka (topic = `events`).
3. Storage runs a Kafka consumer thread to read from topic.
4. Storage writes payload to MySQL.
5. Test by turning Storage off → Receiver still produces. When Storage comes back, it consumes pending messages.

1. Updated docker-compose.yml to add ZooKeeper + Kafka services.
2. Configured Kafka with topic events:1:1 (name, partition, replica).
3. Installed pykafka in Receiver + Storage.
4. Updated Receiver: replaced POST → Storage with Kafka producer.
5. Updated Storage: added Kafka consumer thread to read from topic.
6. Removed old Storage POST endpoints (now events only come via Kafka).
7. Ran Docker Compose, started services, and tested with Swagger + JMeter.

### Pseudocode
```
Receiver:
  connect to Kafka
  produce(event)

Storage:
  connect to Kafka
  for each new message:
    decode payload
    save to DB
    commit offset
```

# End
