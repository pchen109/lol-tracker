
##### Purpose
- Scale Receiver and Storage with a software load balancer (NGINX)
- Move all services to a common endpoint

##### Part 1 - Nginx Config
- copy `nginx.conf` from container to project folder
	- `docker compose cp dashboard:/etc/nginx/conf.d/default.conf ./dashboard/nginx.conf`
- modify the config file
	- default behavior (`/`) 	→ Dashboard UI
	- `/processing`			→ Processing
	- `/analyzer`			→ Analyzer
	- Example
	```
	location / {
		root 	/usr/share/nginx/html;
		index	index.html index.htm;
	}
	
	location /processing {
		proxy_pass http://processing:8100
	}
	
	location /analyzer {
		proxy_pass http://analyzer:8110
	}
	```
- add this line in Dockerfile to overwrite the original `default.conf`
	- `COPY ./nginx.conf /etc/nginx/conf.d/default.conf`

##### Part 2 - Service Endpoints
- change the `base_path` for **ALL** services in their app.py
	- **current**		`app.add_api("openapi.yml", ...)`
	- **changed to**		`app.add_api("openapi.yml", base_path="/receiver", ...) `
- enable/disable CORS with an environment variable
	- ***don't need CORS anymore due to Reverse Proxy Setup***
	- `app.py`
	```py
	if "CORS_ALLOW_ALL" in os.environ and os.environ["CORS_ALLOW_ALL"] == "yes":
		app.add_middleware(...)
	```
	- `docker-compose.yml`
	```yaml
	processing:
		build: processing
		environment:
			CORS_ALLOW_ALL: no
#### Other services with CORS as well
	```
- update config files 
	- Processing should make request to		`http://storage:8090/storage`
	- Dashboard should make request to		`http://cloud-vm-name/processing/stats`
- adjust Docker Compose dependencies accordingly for Nginx service

##### Part 3 - Test and Clean Up
- make following changes
	- only expose the port for the Nginx container to the public
		- → all other services must run using the internal network (not exposed to public)
	- VM firewall should only allow traffic to Nginx forwarded port 
- go through the checklist:
	- Dashboard is accessed via `http://clud-vm-name`
	- Dashboard makes request to the endpoints with correct prefix
		- `http://cloud-vm-name/processing` → check inspector in browser
	- Dashboard updates and displays correct results
	- Services are using an internal Docker network
	- Only accessible service outside the Docker network is Nginx service (port 80)

##### Part 4 - Scale and Test
- run `docker compose up -d --scale receiver=3`
- run `docker compose ps` to check if Receiver has 3 containers running
- update URLs in JMeter or your HTTP test suite
	- http://cloud-vm-name/receiver
	- http://cloud-vm-name/processing 
	- http://cloud-vm-name/analyzer
- send request using JMeter
- check if requested are load balanced
	- `docker compose logs -f receiver`
- change default scaling in `docker-compose.yml` with `deploy` and `replicas`
	```yaml
	services:
		receiver:
			deploy:
				replicas: 3
			build: receiver
		# ...
	```

##### Rubric
- Code
	- single endpoint for all services
	- updated Docker compose with a scaled up services
- JMeter
	- minimum of 100 concurrent threads with 
	- new endpoints
	- Processing and Analyzer are within 5% of the expected values 

##### Knowledge
- The dashboard UI isn’t “inside” the container from the browser’s perspective:
	- The **dashboard container** runs a web server that **serves the dashboard UI (HTML, JS, CSS files)**.
	- When a user opens their browser and goes to `http://cloud-vm-name/`, the browser **downloads that UI code from the dashboard container**.
	- But once the UI (JavaScript) is loaded in the browser, it’s running **on the user’s machine**, outside Docker entirely.
- Proxy
	- Code - `nginx.conf `or `default.conf`
	```nginx
	location /receiver {
		proxy_pass http://receiver:8080;
	}
	```
	- Behavior 
		- a client sends a request to `http://<cloud-vm-name>/receiver`
			- the request first reaches to VM
		- the request gets forwarded to Nginx container
		```yaml
		ports: 
		  - "80:80"
		```
		
		- **proxy part is used here b/t client and VM → not VM internally**

	👉 **Proxy (Nginx) is mainly used between client and VM**  
	→ It handles incoming requests **from the outside**, then routes them **internally** to containers.

# End


- 08/27/2025 - time issue - I should use timestamp, not date_created 
	- need to find out where date_created is coming from
	- likely come from kafka
	- when running docker compose up, date_created is updated using current time
	- b/c i delete the metadata from kafak
	- but I don't get how this change time since rest of the kafka data is still there
	- if this change time, then do i still neeed to keep all the data?
	- check it next
![[Pasted image 20250827090153.png]]