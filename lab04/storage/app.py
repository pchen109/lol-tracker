import connexion
from connexion import NoContent
from datetime import datetime
import threading
from db_init import make_session
from db_model import UserActivity, UserMatch
from db_mgmt import create_tables, drop_tables
import yaml
import logging.config

with open("conf_log.yml", "r") as f:
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
            timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %I:%M:%S.%f %z"),
            trace_id = payload["trace_id"],
        )
    if "match_id" in payload:
        event = UserMatch(
            match_id = payload["match_id"],
            user_id = payload["user_id"],
            kill = payload["kill"],
            death = payload["death"],
            assist = payload["assist"],
            timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %I:%M:%S.%f %z"),
            trace_id = payload["trace_id"],
        )
    session.add(event)
    session.commit()
    session.close()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    drop_tables()     ### used for debug only
    create_tables()
    app.run(port=8090)