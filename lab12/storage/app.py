import connexion
from connexion import NoContent
from datetime import datetime as dt
from sqlalchemy import select
import threading
from db_init import make_session
from db_model import UserActivity, UserMatch
from db_mgmt import create_tables, drop_tables
import yaml
import logging.config
from kafka_consumer import KafkaConsumer
import json
from threading import Thread

with open ("./config/storage_config.yml", "r") as f:
    variables = yaml.safe_load(f.read())
hostname = variables["kafka"]["hostname"]
port = variables["kafka"]["port"]
topic_name = variables["kafka"]["topic"]

with open("./config/logging_config.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

db_lock = threading.Lock()

def add_activity(body):
    with db_lock:
        store_events(body)
    trace_id = body["trace_id"]
    logger.debug(f"SUCCESS DATABASE - add_activity (trace id: {trace_id})")
    return NoContent, 201

def add_match(body):
    with db_lock:
        store_events(body)
    trace_id = body["trace_id"]
    logger.debug(f"SUCCESS DATABASE - add_match (trace id: {trace_id})")
    return NoContent, 201

def store_events(payload):
    session = make_session()
    if "region" in payload:
        event = UserActivity(
            user_id = payload["user_id"],
            region = payload["region"],
            login_counts = payload["login_counts"],
            timestamp = dt.strptime(payload["timestamp"], "%Y-%m-%dT%I:%M:%S.%f%z"),
            trace_id = payload["trace_id"],
        )
    if "match_id" in payload:
        event = UserMatch(
            match_id = payload["match_id"],
            user_id = payload["user_id"],
            kill = payload["kill"],
            death = payload["death"],
            assist = payload["assist"],
            timestamp = dt.strptime(payload["timestamp"], "%Y-%m-%dT%I:%M:%S.%f%z"),
            trace_id = payload["trace_id"],
        )
    session.add(event)
    session.commit()
    session.close()

### KAFKA Consume
consumer = KafkaConsumer(f"{hostname}:{port}", topic_name.encode())
def process_messages():
    for msg in consumer.consume_message():
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)

        payload = msg["payload"]

        if msg["type"] == "add_activity":
            add_activity(payload)
        elif msg["type"] == "add_match":
            add_match(payload)
        consumer.commit()
### End of KAFKA Consume

### THREAD
def setup_kafka_thread():
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
### End of THREAD 

### GET Method
def get_activity(start_timestamp, end_timestamp):
    return get_events(start_timestamp, end_timestamp, UserActivity)

def get_match(start_timestamp, end_timestamp):
    return get_events(start_timestamp, end_timestamp, UserMatch)

def get_events(start_timestamp, end_timestamp, class_name): 
    session = make_session()
    start = dt.fromisoformat(start_timestamp)
    end = dt.fromisoformat(end_timestamp)

    statement = select(class_name)\
        .where(class_name.timestamp >= start)\
        .where(class_name.timestamp < end)
    
    results = [
        result.to_dict() for result in session.execute(statement).scalars().all()
    ]
    
    session.close()
    logger.info("Found %d %s event (start: %s, end: %s)", len(results), class_name.__table__.name , start, end)
    return results, 200
### End of GET Method

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            base_path="/storage",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    drop_tables()     ### used for debug only
    create_tables()
    setup_kafka_thread()
    app.run(port=8090, host="0.0.0.0")