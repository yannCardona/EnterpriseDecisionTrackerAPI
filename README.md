# Project Setup

## Prerequisites

- PostgreSQL
- Python 3.x
- pip


## Setup
1. Clone the repository:

2. Create Database and User in postgreSQL:
	psql -U 'your postgres login'
	CREATE USER postgres_user WITH PASSWORD 'db_1234';
	CREATE DATABASE decisions_db OWNER postgres_user;
	GRANT ALL PRIVILEGES ON DATABASE decisions_db TO postgres_user;
	\q

3. Create and activate virtual environment and install requirements 
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

4. Create and run migrations
	python manage.py makemigrations
	python manage.py migrate

5. run the following script to create an admin and a regular user
	python manage.py shell < create_users.py

6. run the server
	python manage.py runserver

## Use

1. go to http://127.0.0.1:8000/api/docs/ to access the documentation
2. without authentication only the GET API endpoints are accessible 
3. For authentication generate a token with a post request to /api/token/ using one of the following Users
	the User 'admin' (pswd: 'admin'), belongs to the 'Admin' Group and can access all API endpoints
	the User 'user' (pswd: 'u1s2e3r') can't evaluate decisions
4. copy the access token, click the 'Authorize' Button on the upper right and paste it in the value field
5. you should now be able to access all API endpoints
