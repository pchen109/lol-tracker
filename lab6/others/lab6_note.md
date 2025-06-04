
##### Purpose
- set up Docker containers for MySQL
- set up asynchronous message service (Kafka and Zookeeper)
- send message from **Receiver** to **Kafka**
- consume **Kafka** message in **Storage**

##### Part 1 - Docker Environment
- install Docker desktop on your computer or
- install Docker on a cloud VM

##### Part 2 - MySQL, Kafka and Zookeeper
- update/modify `docker-compose.yml` for MySQL, Kafka and Zookeeper
- explanation 
	- `KAFKA_CREATE_TOPICS: "events:1:1"` 
		- topic name: `events`
		- partition: `1`
			- a single piece of a Kafka topic
		- replicas: `1`
			- copies of the partitions → used as data redundancy
	```yaml
	services:
	  zookeeper:
		image: wurstmeister/zookeeper
	  kafka:
		image: wurstmeister/kafka
		command: [start-kafka.sh]
		ports:
		  - "9002:9002"
		environment:
		  KAFKA_CREATE_TOPICS: "events:1:1"
		  KAFKA_ADVERTISED_HOST_NAME: localhost
		  KAFKA_LISTENERS: INSIDE://:29002,OUTSIDE://:9092
		  KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
		  KAFKA_ADVERTISED_LISTENERS: INSIDE://kafka:29092,OUTSIDE://localhost:9092
		  KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
		  KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
		volumes:
		  - /var/run/docker.sock:/var/run/docker.sock
		depends_on:
		  - "zookeeper"
	  db:
		image: mysql
		restart: always
		environment:
		  MYSQL_RANDOM_ROOT_PASSWORD: 1
		  MYSQL_DATABASE: 'riot'
		  MYSQL_USER: 'riot'
		  MYSQL_PASSWORD: 'riot'
		ports:
		  - '3306:3306'
		volumes:
		  - my-db:/var/lib/mysql		### persistent data
	
	volumes:
		my-db:							### volume for data persistence
	```
- run `docker compose up -d` to start services
- run `docker compose up` to check console output for error messages
- run `docker compose ps` to check status of running services
- run `docker compose ps -a` to check if there are an stopped service

##### Part 3 - Produce Messages in `Receiver`
- install `pykafka` module/library 
- update `conf_app.yml` in **Receiver** for **Kafka**
	```yaml
	events:
	  hostname: localhost
	  port: 9092
	  topic: events
	```

###### Produce Messages
- import `KafkaCllient` from `pykafka` in `app.py`
- replace POST request to **Storage** with the following with your own modification in `app.py`
	- `type`: event type
	- `payload`: data received in the request
	- overall, these codes post `msg` to the topic `events` in Kafka
	```python
	client = KafkaClient(hosts='<hostname from conf_app>:<port from conf_app>')
	topic = client.topics[str.encode('<topic from conf_app>')]
	producer = topic.get_sync_producer()
	
	msg = {
		"type": "<your own type of event>",
		"datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
		"payload": reading
	}
	
	msg_str = json.dumps(msg)
	producer.produce(msg_str.encode('utf-8'))
	```
- need to hardcode the status code of your response to 201 (not from POST anymore)

##### Part 4 - Consume Messages in `Storage`
* install `pykafka` module/library
* update `conf_app.yml` in **Storage** for **Kafka**
	```yaml
	events:
	  hostname: localhost
	  port: 9092
	  topic: events
	```
###### Consume Messages
- import `KafkaClient` from `pykafka` in `app.py`
- import `OffsetType` from `pykafka.common`
- add this function below in `app.py` with your own modification
- add logging to help with troubleshooting and debugging
	```python
	def process_messages():
		""" Process event messages """
		hostname = "<hostanem from conf_app>" # localhost:9092
		client = KafkaClient(hosts=hostname)
		topic = client.topics[str.encode("<topic from conf_app>")]
		
		# Create a consume on a consumer group → only reads new messages
		# Only read uncommitted messages when Storage restarts
		consumer = topic.get_simple_consumer(
			consumer_group = b'event_group',
			reset_offset_on_start = False,
			auto_offset_rest = OffsetType.LATEST
		)
		
		for msg in consumer:
			msg_str = msg.value.decode("utf-8")
			msg = json.loads(msg_str)
			logger.info("Message: %s" % msg)
		
			payload = msg["payload"]
		
			if msg["type"] == "event1":
				# store event1 payload in DB
			elif msg["type"] == "event2":
				# store event2 payload in DB
		
			# commit the new message as being read
			consumer.commit_offsets()
	```

###### Create a Thread to Consume Messages
- import `Thread` module/library from `threading` in `app.py`
- add this function in `app.py` to create a thread to consume messages in parallel 
- modify the function as needed
	```python
	def setup_kafka_thread():
		t1 = Thread(target=process_messages)
		t1.setDaemon(True)
		t1.start()
	```
- call this function in `if __name__ == "__main__":` before `app.run` call

##### Part 5 - Clean up and Test
- remove POST for **Storage** in `openapi.yml` and `app.py`
- run HTTP request to **Receiver**
- check events are received and stored to MySQL via Kafka
- verify if you stop and restart **Storage**, the consumer offset is retained
	- It doesn't re-read all messages on topic again 
	- in other words, it won't add **all** past messages from Kafka again 
- run `jMeter` to check everything is working fine

##### Document
- [MySQL Image Docker Hub](https://hub.docker.com/_/mysql)
- [Kafka-Docker Image Docker Hub](https://hub.docker.com/r/wurstmeister/kafka)
- [Zookeeper-Docker Image Docker Hub](https://hub.docker.com/r/wurstmeister/zookeeper)
- [Zookeeper and Kafka](https://dattell.com/data-architecture-blog/what-is-zookeeper-how-does-it-support-kafka/)
- [`pykafka` Installation](https://pykafka.readthedocs.io/en/latest/)
- [`KAFKA_CREATE_TOPICS: "events:1:1"`](https://medium.com/@littl3miss/use-the-init-container-to-create-kafka-topics-70d7d586152#:~:text=KAFKA_CREATE_TOPICS%3A%20%22Topic1%3A1%3A3%22)
- [Kafka Partitions and Replicas](https://rem-baba.medium.com/apache-kafka-partitions-replicas-and-topic-1159391ccf42#:~:text=partitions%20and%20replicas.-,PARTITIONS,-Partitions%3A%20A)
- [Connexion Validate Request by DEFAULT](https://connexion.readthedocs.io/en/stable/validation.html#:~:text=By%20default%2C%20Connexion%20checks%20all%20the%20request%20for%20any%20parameters%20defined%20in%20your%20specification%20and%20validates%20them%20against%20their%20definition.)
- [`strict_validation`](https://connexion.readthedocs.io/en/stable/validation.html#:~:text=You%20can%20turn%20on%20strict_validation%20if%20you%20want%20Connexion%20to%20disallow%20any%20extra%20parameters%20that%20are%20not%20defined%20in%20your%20specification)
	- disallow any extra parameters that are not defined in spec
	- If parameter validation fails, Connexion will return a `400 Bad Request` response with information on the failure in the description

# End