import connexion
from connexion import NoContent
import json
from os import path
from datetime import datetime
import threading

MAX_EVENTS = 5
EVENT_FILE = "events.json"
file_lock = threading.Lock()

def add_activity(body):
    with file_lock:
        log_events(body)
    return NoContent, 201

def add_match(body):
    with file_lock:
        log_events(body)
    return NoContent, 201

def log_events(payload):
    contents = {
        "activity": 0,
        "last_5_activities": [],
        "match": 0,
        "last_5_matches": []
    }
    event_info = {}
    received_timestamp = datetime.now().strftime("%I:%M%p:%S.%f - %a, %b %d. %Y")
    event_info["received_timestamp"] = received_timestamp
    
    if path.exists(EVENT_FILE) and path.getsize(EVENT_FILE) > 0:
        try:
            with open(EVENT_FILE, "r") as fp:
                contents = json.load(fp)
        except json.JSONDecodeError:
            pass
    
    if "region" in payload:
        contents["activity"] += 1

        if len(contents["last_5_activities"]) >= 5:
            contents["last_5_activities"].pop()

        msg_data = f"This user, {payload["user_id"]}, has logged in {payload["login_counts"]} times."

        event_info["msg_data"] = msg_data
        contents["last_5_activities"].insert(0, event_info)
    
    if "match_id" in payload:
        contents["match"] += 1

        if len(contents["last_5_matches"]) >= 5:
            contents["last_5_matches"].pop()

        msg_data = f"This user, {payload["user_id"]}, has {payload["kill"]} kills in this match."
        
        event_info["msg_data"] = msg_data
        contents["last_5_matches"].insert(0, event_info)

    with open(EVENT_FILE, "w") as fp:
        json.dump(contents, fp, indent=4)

    return None

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)