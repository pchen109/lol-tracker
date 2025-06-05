# Lab 6 - Kafka and ZooKeeper
### Tasks
- set up a container for Kafka as asynchronous message service
- set up a container for ZooKeeper to track Kafka cluster/node
- send message from **Receiver** to **Kafka**
- consume **Kafka** message in **Storage**
- remove two POST endpoints of Storage used to receive message from Receiver

### Result
- Kafka, asynchronou message service, is set up
- Storage can be off when Receiver is getting new message
- Storage will consume new message when it's up

### How to Run
1. clone this git repo
2. navigate (`cd`) to lab6 direcotry 
3. run `docker compose up -d`
4. run `app.py` in Storage directory in a console
5. run `app.py` in Receiver directory in another console
6. run `app.py` in Processing directory in another console 
**note**: all consoles running `app.py` would show log messages

### How to Verify Kafka
1. go thru "How to Run" above first.
2. stop Storage and Processing service.
3. run JMeter to send data to Receiver.
4. note current data in MySQL databse.
5. run `app.py` in Storage.
6. check MySQL has new data. 

### How to Use Swagger
###### Receiver
1. access Swagger UI with `http:/localhost:8080/ui`
2. send at least one event from each event type
###### Processing
1. access Swagger UI with `http:/localhost:8100/ui`
2. try `/stats` to get current stats in MySQL database

### How to Use JMeter
1. open JMeter app
2. load `lab6_jmeter.jmx` in `~\lab6\others` directory
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
1. run `docker compose down -v` in lab6 directory
2. stop (`ctrl + c`) `app.py` in both consoles

# End