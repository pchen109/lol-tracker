import connexion
import threading
import httpx
import yaml
import json
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
import httpx
from os import path
from datetime import datetime

with open ("./config/processing_config.yml", "r") as f:
    variables = yaml.safe_load(f.read())
url_activity = variables["urls"]["activity"]
url_match = variables["urls"]["match"]
interval = variables["scheduler"]["interval"]
state_file = variables["state"]["file"]
state_default = variables["state"]["default"]

full_path = path.abspath(state_file)
file_lock = threading.Lock()

with open("./config/logging_config.yml", "r") as f:
    log_setting = yaml.safe_load(f.read())
    logging.config.dictConfig(log_setting)
logger = logging.getLogger("basicLogger")

def get_stats():
    logger.info("==========ℹ️[getting stats starts]ℹ️==========")

    if path.exists(full_path) and path.getsize(full_path) > 0:
        with open (full_path, "r") as f:
            content = json.load(f)
        content_indent = json.dumps(content, indent=4)
        logger.debug("🐞[%s]🐞", content_indent)
        return content, 200
    logger.error("==========❌[Statistics do not exist!]❌==========")
    return {"message": "Statistics do not exist"}, 404

def populate_stats():
    logger.info("==========ℹ️[processing period starts]ℹ️==========")

    if path.exists(full_path) and path.getsize(full_path) > 0:
        with open (full_path, "r") as f:
            content = json.load(f)
    else:
        content = state_default

    t_current = datetime.now()
    t_last = content["last_updated"]

    params = {
        "start_timestamp": t_last,
        "end_timestamp": t_current
    }

    r_activity = httpx.get(url_activity, params=params)
    r_match = httpx.get(url_match, params=params)

    if r_activity.status_code != 200:
        logger.error("==========❌[Activity Response Code → Not 200]❌==========")
        return
    
    if r_match.status_code != 200: 
        logger.error("==========❌[Match Response Code → Not 200]❌==========")
        return 

    r_num_activities = len(r_activity.json())
    logger.info("==========ℹ️[Num Of Received Activities: %s]ℹ️==========", r_num_activities)
    r_num_matches = len(r_match.json())
    logger.info("==========ℹ️[Num Of Received Matches: %s   ]ℹ️==========", r_num_matches)

    r_max_login_counts = max(r_activity.json(), key=lambda activity: int(activity["login_counts"]), default={"login_counts": 0})["login_counts"]
    r_sum_kill = sum(i["kill"] for i in r_match.json())
    c_sum_kill = content["avg_kill"] * content["num_matches"]
    all_matches = content["num_matches"] + r_num_matches
    try:
        avg_kill = (r_sum_kill + c_sum_kill) / all_matches
    except ZeroDivisionError as e:
        avg_kill = 0

    content["num_activities"] += r_num_activities
    content["num_matches"] += r_num_matches
    content["max_login_counts"] = max(int(content["max_login_counts"]), r_max_login_counts)
    content["avg_kill"] = avg_kill
    content["last_updated"] = datetime.isoformat(t_current)
    
    with file_lock:
        with open(full_path, "w") as f:
            json.dump(content, f, indent=4)
    
    logger.info("==========ℹ️[processing period ended]ℹ️==========")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                    'interval',
                    seconds=interval)
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    position=MiddlewarePosition.BEFORE_EXCEPTION,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, host="0.0.0.0")