##### Purpose
- select a sample software project with requirements
- create the API specification for the first service

##### Software Project
- description of the purpose of the software
- two types of events
- guesstimate about the peak number of concurrent events
- types of users with their description

##### API Specification
- assume events will be received regularly with spikes at certain periods of the day
- formerly known as Swagger Specification
- reminder
	- OpenAPI is documentation for a REST API
	- RESTful API and REST API are used interchangeably
	- RESTful API → faithfully follow REST style
	- REST-like API → use POST for all action including fetching data
- access type
	- open (public)			`OpenAPI`
	- partner
	- internal (private)
- design pattern
	- `REST`		architectural style based on HTTP requests
	- `SOAP`
	- `GraphQL` 

##### OpenAPI Specification for RESTful
- Two POST API endpoints to receive each of the two types of events
- Each event should have at least 4 properties
	- one property must be numeric
	- one property must be an identifier (i.e., unique number or UUID)
	- one property must be a date/time of the event

##### `SwaggerHub`
- create and write new API in https://app.swaggerhub.com/
- URLs and `operationId` in OpenAPI
	- URL
	- HTTP method: `POST`, `GET`, `PUT`, `DELETE`
	- Function name: `operationID` 
	- Schema: JSON data for `POST`
	- Response: HTTP code `201`, `400`, etc. 
	```yaml
	paths:
	  /snow/conditions:
		post:
		  summary: reports snow conditions
		  description: Adds a new snow condition report to the system
		  operationId: app.report_snow_conditions
		  requestBody:
			description: Snow Conditions report to add
			content:
			  application/json:
				schema:
				  $ref: '#/components/schemas/SnowConditions'
			responses:
			  "201":
			    description: item created
			  "400":
			    description: invalid input
	```
- **Schema** in OpenAPI
	- schema = data structure
	- contain properties where each has a type and a possible value
	```YAML
	components:
	  schemas:
		SnowConditions:
		  required:
		  - device_id
		  - resort_id
		  - snow_depth
		  - timestamp
		type: object
		properties:
		  device_id:
			type: string
			description: The device ID reporting the snow reading
			format: uuid
			example: d290f1ee-6c54-4b01-90e6-d701748f0851
		  resort_id:
			type: string
			description: Resort ID (name)
			example: Whistler
		  snow_depth:
			type: integer
			description: snow depth reported by the device
			example: 120
		  timestamp:
			type: string
			description: timestamp when snow reading was taken
			format: date-time
			example: 2016-08-29T09:12:33.001Z
	```

# End