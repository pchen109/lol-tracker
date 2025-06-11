
##### Purpose
- use Docker to containerize microservices into self-contained images
- use Docker Compose to deploy microservices

##### Part 1 - Requirements Text File
- create `requirements.txt` files for each service
- **note**: let Python resolve dependencies rather than having a version number
- all services require
	- `connexion[flask]`
	- `connexion[uvicorn]`
	- `connexion[swagger-ui]`
	- shortcut: `connexion[flask,uvicorn,swagger-ui]`
	- `setuptools`
- **Receiver** requires
	- `pykafka`
- **Storage** requires
	- `sqlalchemy`
	- `mysqlclient`
	- `pykafka`
	- `pymysql`
	- `sqlalchemy_serializer`
	- `cryptography`
- **Processing** requires
	- `httpx`
	- `apscheduler`
- **Analyzer** requires
	- `httpx`
	- `pykafka`
- adjust the list above based on your implementation 

##### Part 2 - Dockerfile
- create a `Dockerfile` for each service
	- use `Python` base image
	- copy `requirements.txt` to container
	- install dependencies from from `requirements.txt`
	- run Connexion application (`app.py`)
- **note**: cannot use Python 3.13 for storage due to SQL bug in 3.13. See Reference
- an example of Dockerfile
	```Dockerfile
	FROM python:3
	
	LABEL maintainer="pchen109@my.bcit.ca"
	
	RUN mkdir /app
	
	# Use the cached RUN layer if requriements.txt is not changed
	COPY ./requirements.txt /app/requriements.txt
	
	WORKDIR /app
	
	# Install dependencies
	RUN pip3 install -r requirements.txt
	
	# The coming RUN layer cannot be reused if any file is modified
	COPY . .
	
	# Change permissions and become a non-privileged user
	RUN chown -R nobody:nogroup /app
	USER nobody
	
	# Indicate this service listens to this por t in the container
	EXPOSE 8080
	
	# Entrypoint = run Python
	ENTRYPOINT [ "python3" ]
	
	# Default = run app.py
	CMD [ "app.py" ]
	```

##### Part 3 - Update Docker Compose
- add each service in `docker-compose.yml`
- mark each service with `build` instead of `image`
	- build the service rather than using the image
- add `TZ: US/Pacific` for **Processing** 
	- **Processing** needs PST to grab data from **DB/MySQL** via **Storage**
- example:
	```Dockerfile
	services:
		receiver:
			build:
				context: receiver
				dockerfile: Dockerfile
			ports:
				- 8080:8080
		storage:
			build:
				context: storage
				dockerfile: Dockerfile
			ports:
				- 8090:8090
	```
- change "localhost" in **Kafka** to `kafka`
	- **NOTE:** ==each service is not listening on localhost==
	- `KAFKA_ADVERTISED_HOST_NAME: localhost` 
		- → `KAFKA_ADVERTISED_HOST_NAME: kafka`
	- `KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:29092,OUTSIDE://kafka:9092`
		- → `KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:29092,OUTSIDE://localhost:9092`
- run `docker compose up -d --build` after updating `docker-compose.yml`

###### `docker compose` commands
- `docker compose exec receiver bash`
- `docker compose -u 0 receiver bash`
- `docker compose logs receiver`
- `docker compose logs receiver -n 10`
- `docker compose logs receiver -n 10 -f`
- `docker compose stop receiver`
- `docker compose rm receiver`
- `docker compose rm receiver -v`

##### Part 4 - Update `app.py`
- **note:**
	- each service runs in a container with dedicated network stack
	- ==each service is no longer accessible on `localhost`==
	- ensure `EXPOSE` port is same as the port in `docker-compose.yml` in each service
- update each service to listen on all network interface
	- i.e., `app.run(port=8080, host="0.0.0.0")`

##### Part 5 - Config Files
- **note**
	- Docker Compose network takes care of DNS resolution
		- service names will resolve to IP addresses
	- do NOT use IP address in config files 
	- If `processing` and `storage` are the service names in `docker-compose.yml`
		- **Processing** can access **Storage** by using `http://storage:8090/...`
	- do NOT need to run services on different ports
		- b/c each container has its own IP address
		```yaml
		services:
		  service_a:
		    image: my-service-a
		    ports:
		      - "5000:5000"  # HostPort : ContainerPort
		
		  service_b:
		    image: my-service-b
		    ports:
		      - "5001:5000"  # Different HostPort : Same ContainerPort
		```
- update `URL` in the config files accordingly based on above note

##### Part 6 - Depends On & Health Check
- need to set up dependencies
	- cannot run `receiver` or `storage` without `kafka`
	- cannot run `processing` without `db`
- example:
	```yaml
	storage:
	  ...
	  depends_on:
		db:
		  condition: service_healthy
		kafak:
		  condition: service_started
	db: 
	  ...
	  healthcheck:
	    test: ["CMD", "mysql", "-u", "riot", "-priot", "-e", "USE riot"]
	    interval: 10s
	    retries: 5
	    start_period: 30s
	    timeout: 10s 
	```

##### Part 7 - Test 
- test if all services works as expected. 
- ensure that this is the final structure
	- each service has a separate folder for its code
	- each service has its own config file
	- each service has its own log file
	- all config files are in a dedicated folder
	- all log files are in a dedicated folder
	- services may us named volumes
	- services may bin mounts for data persistence
	```YAML
	.
	├── config
	│	├── log_config.yml
	│	├── receiver_config.yml
	│	├──< ... >
	│	└── storage_config.yml
	├── data
	│	├── database
	│	│ 	└── [...] MySQL files
	│	├── kafka
	│	│	└── [...] kafka files
	│	├── processing
	│	│	└── processing.json
	├── logs
	│	├── receiver.log
	│	├── storage.log
	│	└── <.....>
	├── docker-compose.yml
	├── storage
	│	├── app.py
	│	├── Dockerfile
	│	├── db.py
	│	├── models.py
	│	├── openapi.yml
	│	└── requirements.txt
	└── receiver
		├── app.py
		├── Dockerfile
		├── requirements.txt
	```
- follow this network setup
	- only forward ports for services that are publicly accessible
		- `receiver`
		- `processing`
		- `analyzer`
- **note**:  **persistence volumes**
	- named volumes
		- used for Zookeeper data in our case
	- bind mounts
		- bind a certain directory or file from host inside the container
		- used for all other data in our case: `kafka`, database, config files and logs

###### Persistent Volume Setup: data
- Kafka container uses	`/kafka`
- MySQL uses			`/var/lib/mysql`
- **Processing** uses		JSON file
	- create a bind-mount volume
	- mount the volume in processing container
	- write the JSON file to the path inside the container where the volume is mounted

###### Persistent Volume Setup: Zookeeper and Kafka
- **CASE/ISSUE:**
	- `Kafka` stores a **cluster ID** in `meta.properties`.
	- `ZooKeeper` also stores the **cluster ID** for Kafka.
	- If `ZooKeeper`'s data is lost (e.g., volume deleted), it generates a **new cluster ID**.
	- `Kafka` will **fail to start** because its old ID doesn't match the new one in `ZooKeeper`.
- **FIX**
	1. **Delete** `meta.properties` in the Kafka data directory.
	2. Kafka will **auto-fetch** the new cluster ID from `ZooKeeper` on start-up
	3. ==Create a script to make this all above happened in one command.==
		1. remove: `command: [start-kafka.sh]` in `docker-compose.yml`
		2. add this in `docker-compose.yml`
	```
	command: >
	  sh -c "rm -f ./kafka/kafka-logs-kafka/meta.properties && start-kafka.sh"
	```
* Helpful commands debugging `Kafka` and `ZooKeeper`
	* `docker compose logs kafka -f`
	* `docker compose logs zookeeper -f`
	* `docker compose exec kafka bash`
		* `kafka-topics.sh --describe --bootstrap-server kafka:9092`
		* `kafka-console-consumer.sh --bootstrap-server=kafka:9092 --topic events --partition 0 --offset earliest`

###### Persistent Volume Setup: Config Files
- rename config file relevant to their service
- put all config files in `config` folder
- don't need to rename logging config file
- make sure each service has a log file on (Docker) host

###### Warning: File Permissions and Users
- better to use Linux system as filesystem permission is more coherent
- **never** run services as root
- **never** `chown -R 777` files
- **note**
	- services is running as `nodbody`
	- bind mounts use permission on (Docker) host

##### Reference
- [Bind Mounts vs Named Volumes](https://stackoverflow.com/questions/47150829/what-is-the-difference-between-binding-mounts-and-volumes-while-handling-persist)
- [Dockerfile - Reused if file not Changed](https://www.reddit.com/r/docker/comments/w325au/why_does_the_python_docker_image_recommend/)
- [`app.run(host="0.0.0.0")`](https://www.reddit.com/r/docker/comments/xwfm08/why_do_i_need_to_specify_host0000_when_running_a/)
	- **note**: 
		- the container runs `app.py`
		- the container would be given a random IP
		- `app.run(host="0.0.0.0")` allows `app.py` to listen to any IP
- [Python 3.13 Issue with SQL](https://www.reddit.com/r/learnpython/comments/1ifch9g/does_anyone_have_a_fix_to_this_error/)
- [Docker - Health Check & Depends On](https://docs.docker.com/compose/how-tos/startup-order/)
- [Docker in Docker - Kafka - Unix socket](https://stackoverflow.com/questions/38649298/why-does-kafka-docker-need-to-listen-on-unix-socket)
	- Using Docker from inside a container (called _Docker-in-Docker_) can be insecure and complex, especially when giving it access to the host’s Docker socket.
	- `/var/run/docker.sock:/var/run/docker.sock`

##### Note
- `cat /etc/passwd` 	→ get all users 
- `cat /etc/group` 		→ get all groups
- `adduser kekw`		→ add a user, need root

# End