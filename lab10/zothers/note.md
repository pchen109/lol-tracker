
##### Purpose
- Build a simple Single Page Application (SPA) user interface
- Use Docker container to run this service

##### Part 1 - Dashboard User Interface Requirement
- use plain HTML/JS to build a simple user interface
- call `/stats` API endpoint to display current statistics of **Processing**
- call **Analyzer**'s API endpoint to display:
	- statistics of Analyzer 
	- (at least) one random event from one type
- display a graphic representing your system (i.e., a logo)
- display the last updated time obtained from either `/stats` API endpoint or JS in the browser
- update statistics and Analyzer info every 2 to 4 seconds

##### Part 2 - Vanilla JS for the Dashboard UI
- find an example of a dashboard application using only **Vanilla JS**
	- Vanilla JS: plain JS code written without external libraries like React, Angular, or jQuery.
- adjust URLs in the JS file
- add all required elements in JS file
- use `nginx` Docker image
- create a dedicated Docker image
	```
	FROM nginx
	
	COPY . /usr/share/nginx/html
	```


##### Part 3 - CORS Setup 
- GET HTTP request will fail due to CORS (security reason)
- Add the followings to to disable CORS checking 
	```python
	from connexion.middleware import MiddlewarePosition
	from starlette.middleware.cors import CORSMiddleware
	
	app = FlaskApp(__name__)
	
	app.add_middleware(
		CORSMiddleware,
		position=MiddlewarePosition.BEFORE_EXCEPTION,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	```
- need to rebuild Processing and Analyzer services 
	- `docker compose up --build`
- **note**: insecure setup but okay for this personal project

##### Rubric
- Dashboard UI
	- stats from **Processing**
	- stats from **Analyzer**
	- an Analyzer event for each of the two event types
	- image reflective of your project
- Processing and Analyzer 
	- have CORS disabled
- JMeter
	- send data to change stats on the Dashboard
	- able to run locally
	- able to run on Cloud VM

##### Commands
* `sudo cp -r lab9/* lab10`

##### Documents
- [Connexion Cookbook](https://connexion.readthedocs.io/en/latest/cookbook.html)

##### Note
- `cp` in Linux doesn't copy hidden file

# End