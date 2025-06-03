# Lab 4 - MySQL & Logging & Configuration
### Tasks
- change from SQLite to MySQL
- use docker to create MySQL database contaienr 
- add logging message to track events
- add external configuration to prevent hardcoding and hide sensitive info

### Result
- Services use external configuration file as varaibles.
- Services display customized log message in console.
- Services store customized log message in `app.log`.
- Storage stores data/events sent from Receiver in MySQL databse.

### How to Run
1. clone this git repo
2. navigate (`cd`) to lab4 direcotry 
3. run `docker compose up -d`
4. run `app.py` in Storage directory in a console
5. run `app.py` in Receiver directory in another console
**note**: both consoles running `app.py` would show log messages

### How to Use Swagger
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type

### How to Use JMeter
1. open JMeter app
2. load `lab4_jmeter.jmx` in `~\lab4\others` directory
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

### How to Close
1. run `docker compose down -v` in lab4 directory
2. stop (`ctrl + c`) `app.py` in both consoles

# End