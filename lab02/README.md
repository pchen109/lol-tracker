# Lab 02 - Receiver 
### Tasks
- create receiver service to receive HTTP requests
- use Swagger UI to test one event at a time
- use JMeter to test multiple event concurrently

### Result
- Receiver listens to HTTP requests.
- Reciever stores processed requests in a JSON file.

### How to Run
1. clone this git repo
2. navigate (`cd`) to **lab02** direcotry 
3. run `app.py` in Receiver directory

### How to Use Swagger
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type

### How to Use JMeter
1. open JMeter app
2. load `lab02_jmeter.jmx` in `~\lab02\others` directory
3. change number of threads and loop count for your own needs
4. press start to send events

### How to Verify
1. open `events.json` in `~\lab02\receiver`

### How to Close
1. stop (`ctrl + c`) `app.py`

# End