from pykafka import KafkaClient
from pykafka.common import OffsetType
import logging.config
import connexion
import yaml
import json

with open("./config/analyzer_config.yml", "r") as f:
    variables = yaml.safe_load(f.read())
hostname = variables["kafka"]["hostname"]
port = variables["kafka"]["port"]
topic_name = variables["kafka"]["topic"]

with open("./config/logging_config.yml", "r") as f:
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
    logger.info("Start getting events number.")
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
    result = {
        "num_activity": counter_activity,
        "num_match": counter_match
    }
    logger.info("Finised with [Activity: %s] and [Match: %s]", counter_activity, counter_match)
    return result, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api(
    "openapi.yml",
    base_path="/analyzer",
    strict_validation=True,
    validate_responses=True
)

from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
import os

if "CORS_ALLOW_ALL" in os.environ and os.environ["CORS_ALLOW_ALL"] == "yes":
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_EXCEPTION,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    app.run(port=8110, host="0.0.0.0")