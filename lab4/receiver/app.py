import connexion
import threading
import httpx
import uuid
import yaml
import logging.config

with open ("conf_app.yml", "r") as f:
    variables = yaml.safe_load(f.read())
url_activity = variables["urls"]["activity"]
url_match = variables["urls"]["match"]

with open("conf_log.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

file_lock = threading.Lock()

def add_activity(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id
    logger.info(f"RECEIVED - add_activity (trace id: {trace_id})")
    r = httpx.post(url_activity, json=body)
    logger.info(f"RESPONSE - add_activity (trace id: {trace_id}) has status {r.status_code}")
    return r.text, r.status_code

def add_match(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id
    logger.info(f"RECEIVED - add_match (trace id: {trace_id})")
    r = httpx.post(url_match, json=body)
    logger.info(f"RESPONSE - add_match (trace id: {trace_id}) has status {r.status_code}")
    return r.text, r.status_code

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)