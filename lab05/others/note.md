##### Purpose
- modify **Storage** to allow periodic processing
- create a **Processing** service that
	- contains periodic processing, logging and external config. 
	- stores data in a JSON file

##### Part 1 - Storage Update
###### Description
- add two `GET` endpoints containing a start and end timestamp parameters
- i.e., `GET /<Event>?start_timestamp=<datetime string>&end_timestam=<datetime string>`
	- GET is just a HTTP method 
	- First `/` after GET is just a separator?
	- rest is `URL`
- both endpoints to return a JSON array of all events whose
	- value of `date_crated` column is within the timestamp range

###### OpenAPI YAML
- update OpenAPI YAML file with given template below
	- `state_timestamp`: parameter
	- `end_timestamp`: parameter
	- Response: array of event objects
	```yaml
	get:
	  tags:
	    - devices
	  summary: gets new blood pressure readings
	  operationId: app.get_blood_pressure_readings
	  description: gets blood pressure readings added after a timestamp
	  parameters:
		- name: start_timestamp
		  in: query
		  schema: 
			type: string
			format: date-time
			example: 2016-08-29T09:12:33.001Z
		- name: end_timestamp
		  in: query
		  schema:
			type: string
			format: date-time
			example: 2016-08-29T09:12:33.001Z
	responses:
	  '200':
		description: successfully returned a list of blood pressure events
		content:
		  application/json:
			schmea:
			  type: array
			  items:
				$ref: '#/components/schemas/BloodPressureReading'
	```

###### Common Issues for Timestamp Format
- time zone issues - MySQL database and laptop could have different time zone
- formatting issues - some format has `Z` and some don't
	- `Z` → Zero time zone or UTC
- space issues → space could be converted to `%20` in URLs
- no knowledge of `datetime` library
- potential alternative: user UNIX timestamps but could be complex to set up

###### `app.py`
- code template for `GET` endpoint
	```python
	def get_blood_pressure_readings(start_timestamp, ent_timestamp):
		""" Gets new blood pressure readings between the start and end timestamps """
		
		session = make_session()
		
		start = dt.fromtimestamp(start_timestamp)
		end = dt.fromtimestamp(end_timestamp)
		
		statement = select(BloodPressure)
						.where(BloodPressure.date_created >= start)
						.where(Bloodpressure.date_create < end)
		
		results = [
			result.to_dict()
			for result in session.execute(statment).scalars().all()
		]
		
		session.close()
		
		logger.info("Found %d blood pressure readings (start: %s, end: %s)", len(results), start, end)
	```

###### Test
- run **Storage**'s `app.py`.
- use POST method to send event via Swagger
- use GET method to verify response output in Swagger

##### Part 2 - Processing Service Setup
###### Description
- **Processing** gets event form **Storage**
- **Processing** generates and stores statistics in a JSON file
- **Processing** has at least **FOUR** statistics
	- two must be **cumulative** → not exactly same as total
		- cumulative number for event 1
		- cumulative number for event 2
	- two must be based on numeric values defined in OpenAPI
		- max or min value of some attribute
		- average value (harder to achieve, see rolling average)

###### Start
- crate a `processing` project
- copy an OpenAPI YAML and `app.py` from another service
- install `apscheduler` library for periodic processing

##### Part 3 - OpenAPI YAML - Processing
- modify the YAML file that only has **one GET endpoint** to return statistics
- validate file with `SwaggerHub` or `Postman`
	```YAML
	openapi: 3.0.0
	info:
	  description: This API provides event stats
	  version: "1.0.0"
	  title: Stats API
	  contact:
		email: pchen109@my.bcit.ca
	paths:
	  /stats:
	    get:
	      summary: Get the event stats
	      operationId: app.get_stats
	      description: Gets Blood Pressure and Heart Rate processed statistics
	      responses:
	        '200':
	          description: Successfully returned a list of blood pressure events
	          content:
	    		application/json:
	    		  schema:
	    			type: object
	    			items:
	    			  $ref: '#/components/schemas/ReadingStats'
	    	'400':
	    		description: Invalid request
	    		content:
	    		  application/json:
	    			schema:
	    			  type: object
	    			  properties:
	    				message:
	    				  type: string
	components:
	  schemas:
	  	ReadingsStats:
			required:
			- num_bp_readings
			- max_bp_sys_reading
			- max_bp_dia_reading
			- num_hr_readings
			- max_hr_readings
			properties:
			  num_bp_readings:
				type: integer
				example: 5000000
			  max_bp_sys_reading:
			    type: integer
			    example: 200
			  max_bp_dia_reading:
			    type: integer
			    example: 180
			  num_hr_readings:
			    type: integer
			    example: 50000000
			  max_hr_reading:
				type: integer
				example: 250
			type: object
	```

###### Test
- use `SwaggerHub` to validate syntax/formatting issue.
	- I had lots of typo. It took me hours to fix it. 😭

##### Part 4 - Update `app.py`
- remove unnecessary code
- add a function for the new GET endpoint
- change port to `8100` or other non-used ports 
	- **Receiver** uses `8080`
	- **Storage** uses `8090`
- create a new function to print a message to console
	- for example:
	```python
	def populate_stats():
		print("In funcion populate stats!")
	```
- create another function to set up a periodic call to the function above 
	- for example:
	```python
	from apscheduler.schedulers.background import BackgroundScheduler
	def init_scheduler():
		sched = BackgroundScheduler(daemon=True)
		sched.add_job(populat_stats,
						'interval',
						second=app_config['scheduler']['interval'])
		sched.start()
	```
- call the function before running API service
	- for example:
	```python
	if __name__ == "__main__":
		init_scheduler()
		app.run(port=8100)
	```
- run `app.py` and verify if it works as expected

##### Part 5 - Update `populat_stats()` with rules
- log an `INFO` message indicating periodic processing has started
- read current statistics from the JSON file
	- if the file doesn't exist, use default values
	- get the current datetime
	- get the datetime of the most recent event processed from the JSON file
- query to get all new events from last requested datetime to now
	- user `start_timestamp` and `end_timestamp`
- log an `INFO` message with the number of event received for each event type
- log an `ERROR` message if no 200 response code
- based on the data received:
	- calculate updated statistics
	- write the updated one to the JSON file
		- include timestamp of the most recent event
	- log a `DEBUG` message containing updated statis value
- log an `INFO` message indicating period processing has ended
- set a default value for `start_timestamp` if no JSON file exists
- set up JSON file in this similar format:
	- 203 blood pressure readings
		- max diastolic pressure was 160
		- max systolic pressure was 100
	- 200 heart rate readings
		- max reading was 197
	- most recent event has the `last_updated` timestamp
	```json
	{
		"num_bp_readings": 203,
		"max_bp_dia_reading": 160,
		"max_bp_sys_reading": 100,
		"num_hr_readings": 200,
		"max_hr_readings": 197,
		"last_updated": "2021-02-05T12:39:16"
	}
	```
- **NOTE**: values in JSON file should match values in JSON response 
	- check `GET /stats` endpoint in OpenAPI YAML

##### Part 7 - Implement `GET /stats` endpoint
- log an `INFO` message indicating a request was received
- read JSON file and return 404 if file does not exists 
- log an `ERROR` message ("Statistics do not exist") if file does not exists
- log a `DEBUG` message with the contents of the Python Dictionary
- log an `INFO` message indicating request has completed
- return the statistics with a 200 status code

##### Part 6 - Configuration for Processing
- create new YAML config with similar format like this:
	```yaml
	version: 1
	datastore: 
	  filename: data.json
	scheduler:
	  interval: 5
	eventstores:
	  snow_conditions:
	  	url: http://localhost:8090/snow/conditions
	  life_lines:
	  	url: http://localhost:8090/snow/liftlines
	```

##### Part 7 - Testing
- run all three services
- send events to **Receiver**
	- events should be sent to **Storage** and stored in database
	- **Processing** is updating its statistics
- use **Processing**'s `GET` endpoint to get current statistics

##### Code
- `"timestamp": "${__time(yyyy-MM-dd'T'hh:mm:ss.SSSXXX)}"` → JMeter current time ISO syntax
- `TZ: US/Pacific`	→ Environment Time Zone Set Up in `docker-compos.yml`
- `fromisoformat()` → convert an ISO 8601 format to datetime objects
	- `ISO 8601` string format: 
		- `YYYY-MM-DDThh:mm:ss.sssZ`
		- `YYYY-MM-DDThh:mm:ss.sssXXX`
- `fromtimestamp()` → convert a Unix timestamp to datetime objects
- `git commit --amend -m "messages ..."` - modify last committed message
- `class UserActivity(Base, SerializerMixin):` → give `to_dict()` attribute w/o defining its attribute in the class
- `pip install apscheduler --break-system-packages`
- `r = httpx.get(url, params=params)`
	- `r.status_code`
	- `r.text`
- `path.exists()`
- `path.getsize()`
- `path.abspath()`
- `yaml.safe_load(fp.read())`
- `json.load(fp)`
- `json.dump(content, fp, indent=4)`		file
- `json.dumps(content, indent=4)`			data

##### Documents
- [MySQL Environment Variables](https://dev.mysql.com/doc/refman/8.4/en/environment-variables.html)
- [400 Response Connexion](https://connexion.readthedocs.io/en/stable/validation.html#:~:text=parameter%20validation%20fails%2C-,Connexion%20will%20return%20a%20400%20Bad%20Request%20response,-with%20information%20on)
	- If parameter validation fails, Connexion will return a 400 Bad Request response

##### Issues Solved
- `AttributeError: 'UserActivity' object has no attribute 'to_dict'`
	- fixed with 
		- `pip install SerializerMixin --break-system-packages`
		- `from sqlalchemy_serializer import SerializerMixin`
		- `class UserActivity(Base, SerializerMixin):`
- 

# End