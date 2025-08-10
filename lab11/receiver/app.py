import connexion
import uuid
import yaml
import logging.config
from pykafka import KafkaClient
from datetime import datetime
import json

with open ("./config/receiver_config.yml", "r") as f:
    variables = yaml.safe_load(f.read())
hostname = variables["kafka"]["hostname"]
port = variables["kafka"]["port"]
topic_name = variables["kafka"]["topic"]

with open("./config/logging_config.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

def add_activity(body):
    return add_event(body, "add_activity")

def add_match(body):
    return add_event(body, "add_match")

def add_event(payload, event):
    trace_id = str(uuid.uuid4())
    payload["trace_id"] = trace_id
    logger.info("RECEIVED - %s (trace id: %s)", event, trace_id)

    client = KafkaClient(hosts=f"{hostname}:{port}")
    topic = client.topics[str.encode(topic_name)]
    producer = topic.get_sync_producer()

    msg = {
        "type": event,
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "payload": payload
    }

    msg_str = json.dumps(msg)

    producer.produce(msg_str.encode("utf-8"))
    logger.info("RESPONSE - %s (trace id: %s) has status %s", event, trace_id, 201)
    return msg, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            base_path="/receiver",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")