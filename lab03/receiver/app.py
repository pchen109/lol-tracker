import connexion
import threading
import httpx

file_lock = threading.Lock()

def add_activity(body):
    r = httpx.post("http://localhost:8090/lol/activity", json=body)
    return r.text, r.status_code

def add_match(body):
    r = httpx.post("http://localhost:8090/lol/match", json=body)
    return r.text, r.status_code

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)