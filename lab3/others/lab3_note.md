
##### Purpose
- create a storage service to store events in a database
- integrate receiver service with storage service

##### Part 1 - Storage Service 
- **Database Per Service Pattern** - a pattern in microservice
- create a **Storage** folder/project in the same directory of **Receiver**
- copy `openapi.yml` and `app.py` from **Receiver** to **Storage**
- install `sqlalchemy` for ORM features
	- object-relational mapping - stateless database

###### 01. Create Database
- create a `db_init.py` for a database
- set up a database by using `SQLAlchemy` with `SQLite` to define and map models 
	- `SQLite` - a relational database engine
	- `SQLAlchemy` - is a python library
	- the model require a database **engine** and a **session**
	```python
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	
	engine = create_engine("sqlite:///lol-tracker.db")
	
	def make_session():
		retrun sessionmaker(bind=engine)()
	```

###### 02. Create Model
- create a `db_model.py` based on example provided
	- must contain `data_created` column
	- modify the example below to fix your application
	```python
	from sqlalchemy.orm import DeclarativeBase, mapped_column
	from sqlalchemy import Integer, String, DateTime, func
	
	class Base(DeclarativeBase):
		pass
	
	class SnowReport(Base):
		__tablename__ = "snow_report"
		id = mapped_column(Integer, primary_key=True)
		device_id = mapped_column(String(50), nullable=False)
		resort_id = mapped_column(String(50), nullable=False)
		depth = mapped_column(Integer, nullable=False)
		timestamp = mapped_column(DateTime, nullable=False)
		date_created = mapped_column(DateTime, nullable=False, default=func.now())
	```

###### 03. Create Table Management
- create `db_mgmt.py`
- import `sys`
- import `engine` from `db_init.py`
- import `Base` from `db_modle.py`
- create all required tables
	- `Base.metadata.create_all(engine)`
- drop all required tables
	- `Base.metadata.drop_all(engine)`
- use `sys.argv` and `sys.argv[1]` to drop tables
	```python
	import sys
	from models import Base
	from db import engine
	
	def create_tables():
		Base.metadata.create_all(engine)
	
	def drop_tables():
		Base.metadata.drop_all(engine)
	
	if __name__ == "__main__":
		if len(sys.argv) > 1 and sys.argv[1] == "drop":
			drop_tables()
		create_tables()
	```

###### 04. Modify `app.py`
- change port number to `8090` or other number not same as **Receiver**
- modify **POST** method to create and store an event in the database
	- remember to create and close the session
	```python
	def my_openapi_function(body):
		session = make_session()
		event = SnowReport(
			### ... create the event using the attributes received in JSON
		)
		session.add(event)
		session.commit()
		session.close()
	```
- optional - create a **decorator** that handle the session management automatically
	- use `@use_db_session` for your functions
	- ==too hard to understand== 😭
	```python
	def use_db_session(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			session = make_session()
			try:
				return func(session, *args, **kwargs)
			finally:
				session.close()
		
		return wrapper
	```

###### 05. Test API Endpoints
- send HTTP request with **Swagger UI** 
- check records in the database
	- use `DB Browser for SQLite` extension to view the result

##### Part 2 - Integration
- Goal: 
	- **Receiver** makes a HTTP request to **Storage** when a request is sent to **Receiver**
	- **Storage** saves the data in database

###### Modify `receiver`
- install `httpx` library
- use `httpx.post` to access **Storage**'s POST endpoints
	- note: **Storage** use port `8090`
- send event data as JSON payload with `Content-Type` header set to `application/json`
	- user `json` parameter with `httpx`
	- `r = httpx.post("http://localhost:8090/event1", json=data)`
- return `NoContent` and HTTP status code received from storage service
- remove code of writing request to the JSON file

###### Test Both Services
- test **Receiver**'s POST API endpoints
- verify requests are stored in the database

##### Part 3 - Load Testing
- Update `JMeter` to send randomized data
	- [guide](https://jmeter.apache.org/usermanual/functions.html) to use random variables in `JMeter`
		- check `Random`, `RandomDate`, `RandomString`, `UUID`
	- also use CSV files with all possible values as a source for variables

##### Part 4 - Reflection
- Explain errors when running `JMeter` against **Receiver**
	- errors could be seen in the results and in the console for **Storage**
	- **ANSWER**: I didn't see any error when running `JMeter` against receiver. If there were errors, the issues likely would be that `SQLite` couldn't handle large request of data due to race condition issue. I used `threading.Lock()` to prevent the race condition from happening. 
- Why may `SQLite` not be a good choice of database needed high load?
	- **ANSWER**: As mentioned above, `SQLite` can have race condition. " If file locking does not work correctly, two or more clients might try to modify the same part of the same database at the same time, resulting in corruption" ([SQLite Issue](https://www.sqlite.org/whentouse.html#:~:text=If%20there%20are%20many%20client,performance%20will%20not%20be%20great.))
		- Issue: `SQLite` only supports one write at a time per database file.
- What would be a better chose and why?
	- `MySQL` supports concurrent read/write depends on storage engine.
		- `InnoDB` - row-level locking
		- `MyISAM` - table-level locking
	- [source link](https://stackoverflow.com/questions/32087233/how-does-mysql-handle-concurrent-inserts)

##### Code
- `cp -r lab2/* lab3` - only copy files, no lab2 folder in lab3
- `len(sys.agrv)` - number of arguments after `python3`, `py` or `python` in console
	- `python app.py` → `len(sys.agrv)` is 1
	- `python app.py haha` → `len(sys.agrv)` is 2
- `sys.argv[1]`	- second argument
	- `python app.py drop` → `sys.argv[1]` is "drop"

##### Documents
- [JMeter Timestamp](https://www.perfmatrix.com/jmeter-timestamp/)
- [JMeter CSV Random](https://www.blazemeter.com/blog/random-variables-in-jmeter#:~:text=Reading%20the%20Values%20from%20a%20CSV%20file)

# End