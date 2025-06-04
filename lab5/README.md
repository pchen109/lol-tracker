# Lab 5 - Processing Service 
### Tasks
- add two GET endpoints with parametes in Storage for Processing
- set up local time zone in MySQL database and use timestamp properly
- set up Processing with logging and external config
- use Processing service to access Storage periodically
- use Processing service to generate stats and store them in a JSON file
- add all `app.log` and `data.json` in `.gitignore` file

### Result
- Processing checks if MySQL database has new data via Storage periodically.
- Processing generates stat based on the data.
- Processing uses logging to track info.
- Processing uses external config file as variables.
- Storage has two GET endpoints to access data from MySQL database.
- Storage uses timestamp to get new data since the last check.
- MySQL Database uses Pacific timezone.
- Log files are not uploaded to Github anymore.

### How to Run
1. clone this git repo
2. navigate (`cd`) to lab5 direcotry 
3. run `docker compose up -d`
4. run `app.py` in Storage directory in a console
5. run `app.py` in Receiver directory in another console
6. run `app.py` in Processing directory in another console
**note**: all consoles running `app.py` would show log messages

### How to Verify Processing Service Functionality
1. go thru "How to Run" above first.
2. note the current stats in `data.json` of Processing service
3. run JMeter to send data to Receiver.
4. check `data.json` in Processing to verify sent data matches stats.

### How to Use Swagger for Receiver and Processing
###### Receiver
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type
###### Processing
1. access Swagger UI with `http:/localhost:8100/ui`
2. try `/stats` to get current stats in MySQL database

### How to Use JMeter
1. open JMeter app
2. load `lab5_jmeter.jmx` in `~\lab5\others` directory
3. change number of threads and loop count for your own needs
4. press start to send events

### How to Check Data in MySQL
1. access MySQL DB with `docker compose exec -it db mysql -u riot -priot`
2. run `USE riot;`
3. run `select * from user_activity` to see the sent events
4. run `select * from user_match` to see the sent events

### How to Check Log Messages
1. check Receiver log messages from `app.log` in Receiver directory
2. check Storage log messages from `app.log` in Storage directory
3. check Processing log message from `app.log` in Processing directory

### How to Close
1. run `docker compose down -v` in lab4 directory
2. stop (`ctrl + c`) `app.py` in both consoles

# End