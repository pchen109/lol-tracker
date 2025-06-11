# Lab 8 - Docker (Contanization)
### Tasks
- move all logs to a dedicated log folder
- move all config files to to a dedicated config folder
- mount Kafka, MySQL and Processing data to a dedicated data folder
- set correct owner instead of giving permission to OTHERS 
- add Dockerfile and requirements.txt for each services
- **build** each service with their Dockerfile and requirements.txt

### Result
- All services are containizered. 
- Kafka, MySQL and Processing have consistent data.
- Each service has its own software installed.
- All config files are stored in the same folder.
- All log files are stored in the same folder.
- All data are stored in the same folder.
- Each service communicate with each internally → no localhost

### How to Run
1. clone this git repo
2. navigate (`cd`) to lab8 direcotry 
3. run `docker compose up -d`

### How to verify
1. run `docker compose ps -a` to verify all services are running
2. use JMeter to send data to Receiver
3. access MySQL databse container to verify data are matched
4. access `http:/localhost:8100/stats` to verify stats are matched
5. access `http:/localhost:8110/stats` to verify stats are matched
6. use `http:/localhost:8110/activity?index=0` to verfiy data info at index 0
   1. change index number to check further
7. use `http:/localhost:8110/match?index=0` to verify data info at index 0
   1. change index number to check further
8. check all logs in log folder to verify they are receiving logs

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
2. load `lab8_jmeter.jmx` in `~\lab8\others` directory
3. change number of threads and loop count for your own needs
4. press start to send events

### How to Check Events in MySQL
1. access MySQL DB with `docker compose exec -it db mysql -u riot -priot`
2. run `USE riot;`
3. run `select * from user_activity` to see the sent events
4. run `select * from user_match` to see the sent events

### How to Close
1. run `docker compose down -v` in lab8 directory
2. stop (`ctrl + c`) `app.py` in both consoles

# End