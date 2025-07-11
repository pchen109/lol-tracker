
##### Purpose
- add logging and configuration to services
- change to MySQL database from SQLite

##### Part 1 - Switch to MySQL
###### Run a Docker container
- create a new Docker Compose file
	- start from below
	- change user, password and database values
	- note that value 1 in password would be generated 
	```docker
	services:
	  db:
		image: mysql
		environment: 
		  MYSQL_RANDOM_ROOT_PASSOWRD: 1
		  MYSQL_USER: riot
		  MYSQL_PASSWORD: riot
		  MYSQL_DATABASE: riot
		ports:
		  - 3306:3306
	```
- run `docker compose up -d`
	- a `MySQL` instance can be assessed on port `3306`

###### **Storage** using the MySQL instance
- install a MySQL connector
	- **Windows** options - only need one
		- `mysqlclient`	(recommended but could be complicated w/o wheel package)
		- `mysql-connector-python`
		- `pymysql` (easier to set up)
	- **Linux** (WSL) - get all packages below
		- `sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential`
			- need `pkg-config` as "`Trying pkg-config --exists mysqlclient`" error message when trying to install `mysqlclient`
		- `pip install mysqlclient --break-system-packages` - not sure if this is needed
- change **Storage** to use MySQL
	- change the URL for `engine` in database setup
	- syntax: `mysql://<username>:<password>@localhost/<db_name>`
	- need `pymysql` for Linux as `python-mysqldb` is not supported by Python 3 version in Ubuntu 
		- `engine = create_engine("mysql+pymysql://riot:riot@localhost/riot")`
		- `pymysql` is pure Python and has better support

###### Test Storage Service
- run `py app.py` 
- access Swagger UI on browser with `/ui`
- send an event from the UI
- verify that data is stored in the MySQL database
	- `docker compose db mysql -u riot -priot`
	- `use riot;`
	- `show tables;`
	- `select * from user_activity;`

##### Part 2 - Tracing
###### Generate a trace ID and add it to the event
- **Options**
	- 1. use `time` → returned value is **number**
		- `import time`
		- `trace_id = time.time_ns()`	(nanoseconds)
	- 2. use `uuid` → returned value is **string**
		- `import uuid`
		- `trace_id = str(uuid.uuid4())`
- add `trace_id` to the JSON payload in **Receiver**
	- `trace_id` is a unique identifier

###### Update Storage to store the trace ID
- add `trace_id` in OpenAPI YAML for **Storage**
- add `trace_id` column in the `db_model.py` and `app.py`
- note: need to drop and recreate table with updated schema

##### Part 3 - Configuration `Receiver`
- create a new YAML `conf_app.yml`
	```yaml
	version: 1
	eventstore1:
	  url: http://localhost:8090/my-first-event
	eventstore2:
	  url: http://localhost:8090/my-second-event
	```
	- `eventstore1` holds the URL of first event's endpoint
	- `eventstore2` holds the URL of second event's endpoint
- modify  `app_conf.yml` to provide relevant name
	```YAML
	version: 1
	events:
	  snow:
		url: http://localhost:8090/my-first-event
	  lift:
		url: http://localhost:8090/my-second-event
	```
- import `yaml` in `app.py`
- load `app_conf.yml` in `app.py`
	```Python
	with open("app_conf.yml", "r") as f:
		app_config = yaml.safe_load(f.read())
	```
- replace hardcoded URLs in `httpx.post` calls

##### Part 4 - Logging `Receiver`
###### Logging Config File
- create a new YAML file (`log_conf.yml`)
	```yaml
	version: 1
	formatters:
	  simple:
		format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	handlers:
	  console:
		class: logging.StreamHandler
		level: DEBUG
		formatter: simple
		stream: ext://sys.stdout
	  file:
		class: logging.FileHandler
		level: DEBUG
		formatter: simple
		filename: app.log
	loggers:
	  basicLogger:
		level: DEBUG
		handlers: [console, file]
		propagate: no
	root:
	  level: DEBUG
	  handlers: [console]
	disable_existing_loggers: false
	```
- add `import logging.config`
- load `log_conf.yml` in `app.py`
	- `logging.config.dictConfig(config)` - take config from a dictionary/JSON
	```python
	with open("conf_log.yml", "r") as f:
		LOG_CONFIG = yaml.safe_load(f.read())
		logging.config.dictConfig(LOG_CONFIG)
	```

###### Log Messages
- create a logger from `basicLogger` in the config file
	- `logger = logging.getLogger('basicLogger')`
- log a message when an event is received with `INFO` level
	- `RECEIVED - snow_report (trace id: 123456789)`
- log the response message from **Storage** with `INFO` level
	- `RESPONSE - snow_report (trace id: 123456789) has status 201`
- note: all log messages on `logger` → written in console and `app.log`

##### Part 5 - Config and Logging for `Storage`
###### Configuration
- create a YAML file (`conf_app.yml`) for database credentials
	```yaml
	version: 1
	database:
	  user: riot
	  password: riot
	  hostname: localhost
	  port: 3306
	  db_name: riot
	```
- load `app_conf.yml` in `db_init.py` the same way as receiver
- replace hardcoded credentials with variables
###### Logging
- copy `log_conf.yml` file from **Receiver** to **Storage**
- load `log_conf.yml` and create a `logger` object
- use `DEBUG` level to log a message for a successful event after DB session is closed
	- i.e., `SUCCESS store event - snow_report (trace id: 123456789)`

##### Part 6 - Testing
- test services with Postman or Swagger
- test services with `JMeter`
- verify that log messages are written to `app.log` in both services

##### Code
- `str(uuid.uuid4())` - UUID in String
	- `uuid.uuid4()` - UUIS object
- `time.time_ns()` - nanoseconds in Number
- `yaml.safe_load(f.read())`	- convert YAML to PY object in JSON format
- `logging.config.dictConfig(config)` - add config in dictionary format to logging
- "The Boolean variables including `MYSQL_RANDOM_ROOT_PASSWORD` are made true by setting them with any strings of nonzero lengths. Therefore, setting them to, for example, “0”, “false”, or “no” does not make them false, but actually makes them true. This is a known issue." ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/docker-mysql-more-topics.html#:~:text=The%20boolean%20variables,a%20known%20issue.))
- `sudo apt list --installed`
- `suod apt-get install --upgrade <pkg>`
- `sudo apt install python-is-python3`
- `wsl --install -d ubuntu --name <machine-name>`
- `wsl ~ -d test`
- `engine = create_engine("mysql+pymysql://riot:riot@localhost/riot")`
- `alias py=python3` in `~/.bashrc`
- `import logging.config`
- `import uuid`

##### Documents
- [`MYSQL_RANDOM_ROOT_PASSWORD`](https://dev.mysql.com/doc/refman/8.4/en/docker-mysql-more-topics.html#:~:text=The%20boolean%20variables,a%20known%20issue.)
- [MySQL Engine](https://docs.sqlalchemy.org/en/20/core/engines.html#:~:text=at%20PostgreSQL.-,MySQL,-%C2%B6)
- [`logging.config.dictConfig(config)`](https://docs.python.org/3/library/logging.config.html)
- [YAML Safe Load](https://python.land/data-processing/python-yaml#PyYAML_safe_load_vs_load:~:text=(yaml)-,Convert%20YAML%20to%20JSON%20using%20Python,-If%20you%20need)
- [JSON and Python Object](https://www.geeksforgeeks.org/python-json/#:~:text=Convert%20from%20JSON%20to%20Python%20object)
- [`PyMySQL` vs `MySQLdb`](https://stackoverflow.com/questions/7224807/what-is-pymysql-and-how-does-it-differ-from-mysqldb-can-it-affect-django-deploy#:~:text=PyMySQL%20and%20MySQLdb%20provide%20the%20same%20functionality%20%2D%20they%20are%20both%20database%20connectors.%20The%20difference%20is%20in%20the%20implementation%20where%20MySQLdb%20is%20a%20C%20extension%20and%20PyMySQL%20is%20pure%20Python.)

# End