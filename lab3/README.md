# Lab3 - Storage with SQLite & Integration
### Tasks
- create storage service with SQLite
- integrate storage service with receiver
- set up random varaibles in JMeter

### Result
- Receiver sends the request to Storage when getting HTTP request
- Storage stores the event sent from Receiver in SQLite database
- JMeter automatically send events with different values

### How to run 
1. clone thhis git repo
2. navigate (`cd`) to lab3 direcotry 
3. run `app.py` in Storage directory in a console
4. run `app.py` in Receiver directory in another console

### How to Use Swagger
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type

### How to Use JMeter
1. open JMeter app
2. load `lab3_jmeter.jmx` in `~\lab3\others` directory
3. change number of threads and loop count for your own needs
4. press start to send events

### How to Check Events
1. access `lol-tracker.db` with SQLite Viewer extension in `~\lab3\storage`

### How to Close
1. stop (`ctrl + c`) `app.py` in both consoles

# End