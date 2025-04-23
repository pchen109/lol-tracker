
##### Purpose
- build a Receiver Service that 
	- receive two event types
	- store two them in a JSON file
- test the service with PostMan & Apache JMeter

##### Part 1 - connexion
- create `receiver` project		→ i.e., a folder named `receiver`
- install following packages 
	- might need `--break-system-packages` if installed in Linux/Ubuntu
	- `connexion[flask]`
	- `connexion[uvicorn]`
	- `swagger-ui-bundle`		→ swagger UI endpoint
- use `openapi.yml` from lab1
- create a connexion app in `app.py`
	- name the function based on the `operationId`
	- **must** use `body` as an argument for payload data sent to an endpoint
	- display the payload to the console with `print()`
	- return a 201 response code. i.e., `return NoContent, 201`
	```python
	import connexion
	from connexion import NoContent
	
	def my_first_openapi_function(body):
		# Write your code here
	
	# Define all required functions
	
	app = connexion.FlaskApp(__name__, specification_dir='')
	app.add_api("my-open-api-file.yml")
	
	if __name__ == "__main__":
		app.run(port=8080)
	```
- run the connexion app and check result from `http://localhost:8080/ui`
- use PostMan to verify both API endpoints

##### Part 2 - Log Event Data to a File
- remove print statements
- store recent events in a `events.json` file
	- total number of Type 1 events
	- total number of Type 2 events
	- last 5 events for Type 1 → newest on top
	- last 5 events for Type 2 → newest on top
- store this content for each event
	- `received_timestamp`: current date and time 
		- use `datetime` get current date and time
		- use `strftime` to format it to a string
	- `msg_data`: strings containing at least two properties of the event
- note these rules
	- cannot store more than 5 events for each type
	- only one JSON file
- create a function to store data as described above into the JSON file
	- consume the new event
	- load the older data from the JSON file
	- update file with new event
	- use a constant (i.e., `MAX_EVENTS`) to define the max number of events to store
	- use a constant (i.e., `EVENT_FILE`) to define the filename where events are stored
- example of the JSON file
	```JSON
	{
		"num_bp": 1,
		"recent_bp": [
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a BP of 120/80.",
				"received_timestamp": "2024-01-15 07:35:22.075212"
			}
		],
		"num_hr": 10,
		"recent_hr": [
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a heart rate of 85.",
				"received_timestamp": "2024-01-15 07:36:10.026523"
			},
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a heart rate of 86.",
				"received_timestamp": "2024-01-15 07:36:09.482410"
			},
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a heart rate of 81.",
				"received_timestamp": "2024-01-15 07:36:08.045196"
			},
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a heart rate of 89.",
				"received_timestamp": "2024-01-15 07:36:07.579387"
			},
			{
				"msg_data": "Patient d290f1ee-6c54-4b01-90e6-d701748f0851 with a heart rate of 78.",
				"received_timestamp": "2024-01-15 07:36:06.584571"
			}
		]
	}
	```

##### Part 3 - Strict Validation
- enable validation on the request and response of the API
- add the following arguments to the `add_api` call
	- `strict_validation=True`
	- `validate_responses=True`
- verify API still works
- verify that invalid messages should be rejected

##### Part 4 - Test the Service
- install [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)
	- download the latest binary
	- must need Java 8 installed 
	- run the `.bat` (Windows) or `.sh` (Linux) file from the bin folder
- create a `Test Plan` with **ONE** `Thread Group`
- **Thread Group**
	- set `number of threads` to expected peak load of concurrent event
	- set `loop count` to 10
- **Headers**
	- add HTTP Head Manger 
		- right click → select Add > Config Element > HTTP Header
	- set Content-Type of the request body to `application/json`
- add **View Results Tree** to view results in the Thread Group

##### Documents
- [Race Condition](https://medium.com/yavar/understanding-race-conditions-in-python-and-how-to-handle-them-98f998708b2c)
- [JMeter Setup for `application/json`](https://www.redline13.com/blog/2020/03/jmeter-load-testing-with-a-json-payload/)
- [JMeter tutorial](https://www.blazemeter.com/blog/rest-api-testing)
- [JMeter Built-In Functions and Variables](https://jmeter.apache.org/usermanual/functions.html)

##### Code
- `hostname -i`		IP of localhost
- `strftime()`		convert datetime to string
- `datetime.now()`	current time in datetime object
- `json.dump(content, fp)`	no "s" → save content to a file
- `json.load(fp)`				no "s" → read content from a file
- `file_lock = thread.Lock()`
	- need this to deal with **race condition**.

# End