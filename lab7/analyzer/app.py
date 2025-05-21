from pykafka import KafkaClient
from pykafka.common import OffsetType
import logging.config
import connexion
import yaml
import json

with open("conf_app.yml", "r") as f:
    variables = yaml.safe_load(f.read())
hostname = variables["kafka"]["hostname"]
port = variables["kafka"]["port"]
topic_name = variables["kafka"]["topic"]

with open("conf_log.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

def get_activity_index(index):
    return get_event_index(index, "add_activity")

def get_match_index(index):
    return get_event_index(index, "add_match")

def get_event_index(index, event):
    logger.info("Start looking up %s at index %d", event, index)
    client = KafkaClient(hosts=f"{hostname}:{port}")
    topic = client.topics[topic_name.encode()]
    consumer = topic.get_simple_consumer(consumer_timeout_ms=1000)

    counter = 0
    for msg in consumer:
        message = msg.value.decode("utf-8")
        data = json.loads(message)
        payload = data["payload"]
        
        if data["type"] == event:
            if index == counter:
                logger.info("Event %s is found at index %d", event, index)
                return payload, 200
            counter += 1
        elif data["type"] == event:
            if index == counter:
                logger.info("Event %s is found at index %d", event, index)
                return payload, 200
            counter += 1
        
    logger.info("No %s found at index %d", event, index)
    return { "message": f"No {event} found at index {index}!"}, 404

def get_event_stats():
    client = KafkaClient(hosts=f"{hostname}:{port}")
    topic = client.topics[topic_name.encode()]
    consumer = topic.get_simple_consumer(consumer_timeout_ms=1000)

    counter_activity = 0
    counter_match = 0
    for msg in consumer:
        message = msg.value.decode("utf-8")
        data = json.loads(message)
        if data["type"] == "add_activity":
            counter_activity += 1
        elif data["type"] == "add_match":
            counter_match += 1
    return {
        "num_activity": counter_activity,
        "num_match": counter_match
    }, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(
    "openapi.yml",
    strict_validation=True,
    validate_responses=True
)

if __name__ == "__main__":
    app.run(port=8110)