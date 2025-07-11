# Lab 07 - Analyzer
### Tasks
- create a new service, Analyzer, that consumes message from Kafka
- use logging to track info in Analyzer
- use external config as variables in Analyzer
- use a GET endpoint to get info of event1 at a specified index
- use a GET endpoint to get info of event2 at a specified index
- use a GET endpoint to get an overall info of both events

### Result
- Analyzer uses external configuration file as varaibles.
- Analyzer displays customized log message in console.
- Analyzer displays event1 at a specified index.
- Analyzer displays event2 at a specified index.
- Analyzer displays an overall info of both events.

### How to Run
1. clone this git repo
2. navigate (`cd`) to **lab07** direcotry 
3. run `docker compose up -d`
4. run `app.py` in Storage directory in a console
5. run `app.py` in Receiver directory in another console
6. run `app.py` in Processing directory in another console
7. run `app.py` in Analyzer directory in another console
**note**: both consoles running `app.py` would show log messages

### How to Verify Analyzer
1. go thru "Hot to Run" above first
2. use JMeter to feed some data to Kafka
3. enter `localhost:8110/stats` to gather overal events info
4. enter `localhost:8110/activity?index=0` to get user activity at index 0
   1. if index doesn't have info → status 401 and "not available" message
5. enter `localhost:8110/match?index=0` to get user match at index 0
   1. if index doesn't have info → status 401 and "not available" message
6. use `app.log` in Analyzer to track info 

### How to Use Swagger
###### Receiver
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type
###### Processing
1. access Swagger UI with `http:/localhost:8100/ui`
2. try `/stats` to get current stats in MySQL database
###### Analyzer
1. access Swagger UI with `http:/localhost:8110/ui`
2. modify index to get info of one of events in `/activity`
3. modify index to get info of one of events in `/match`
4. try `/stats` to get overall info of both events

### How to Use JMeter
1. open JMeter app
2. load `lab07_jmeter.jmx` in `~\lab07\others` directory
3. change number of threads and loop count for your own needs
4. press start to send events

### How to Check Events in MySQL
1. access MySQL DB with `docker compose exec -it db mysql -u riot -priot`
2. run `USE riot;`
3. run `select * from user_activity` to see the sent events
4. run `select * from user_match` to see the sent events

### How to Check Log Messages
1. check Receiver log messages from `app.log` in Receiver directory
2. check Storage log messages from `app.log` in Storage directory
3. check Processing log messages from `app.log` in Processing directory
4. check Analyzer log messages from `app.log` in Analyzer directory

### How to Close
1. run `docker compose down -v` in lab07 directory
2. stop (`ctrl + c`) `app.py` in both consoles

# End