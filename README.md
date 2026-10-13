Project Description

This project is a Meeting Room Booking System developed for Software Security Assignment 1.
The application allows users to book meeting rooms, view their reservations, cancel them and reschedule them. Normal users can manage their own reservations,
while administrators have additional permissions to manage reservations belonging to other users.
The system contains three meeting rooms. Bookings are allowed on weekdays from 09:00 to 17:00, and each reservation lasts exactly one hour.
The main goal of this project is to implement a functional application while focusing on secure software development, authentication, authorization and security between different components.

Architecture

The application consists of three independent components that will communicate throught HTTP APIs using JSON.

	Application API (port 8000): Handles user authentication, user roles and coordinates requests between the services.
	Reservation Service (port 8001): Manages reservations, checks room availability and verifies that users have permissions to access or modify reservations. It is the only service with direct access to the Reservation Database.
	Scheduling Service (port 8002): Validates booking dates, times and duration based on predefined scheduling rules. It will use a separately installable helper package.

The application will use SQLite for data storage and JWT tokens for authentication between requests.

More information about the system design and security decisions can be found in the docs/ folder.

Technologies
	Python 3.14.7
	FastAPI
	SQLite
	HTTP/JSON
	Pytest
	PyJWT
	pwlib (Argon 2 password hashing)
	Jenkins (planned)

Installation
The project is developed using Python and FastAPI.

First clone the repository and open the project folder.

Create a Python virtual environment:

py -m venv .venv

Install the project dependencies:

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Initialize the Authentication Storage:

.\.venv\Scripts\python.exe application_api\init_auth_db.py

This creates the SQLite database with three predefined user accounts:
Alice and Bob as normal users and Admin as an administrator.
Password are stored as Argon2 hashes.


Running the application

Before starting the Application API, configure the JWT signing key in Terminal 1:

$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"

This key is generated randomly and stored as an environment variable for the current terminal session.

The three components run as separate processes. Open three terminals in the project root directory and execute the following commands.
	Application API - Terminal 1
	.\.venv\Scripts\python.exe -m uvicorn application_api.main:app --reload --host 127.0.0.1 --port 8000
	
	Reservation Service - Terminal 2
	.\.venv\Scripts\python.exe -m uvicorn reservation_service.main:app --reload --host 127.0.0.1 --port 8001
	
	Scheduling Service - Terminal 3
	.\.venv\Scripts\python.exe -m uvicorn scheduling_service.main:app --reload --host 127.0.0.1 --port 8002
	
To verify that the components are running, open the following URLs:

	Application API: http://127.0.0.1:8000/health
	Reservation Service: http://127.0.0.1:8001/health
	Scheduling Service: http://127.0.0.1:8002/health

Each endpoint should return {"status": "ok"}.

Testing 
The project uses pytest for automated testing.
To run the test, execute the following command from the project root:
.\.venv\Scripts\python.exe -m pytest tests/ -v

The current tests cover scheduling validation, working hours, date and time validation, the helper package, the Scheduling Service API and user authentication.
authentication tests verify successful login, incorect passwords and unknown users.

Current Progress

The project is currently under development.

The three independent FastAPI components have been created and tested using their health check endpoints

The Scheduling Service now validates booking dates and times according to the predefined rules. It also uses a separately installable  helper package to calculate reservation ending times.

The Scheduling Service provides a POST /validate endpoint and has automated tests using pytest.

The Application API now supports user authentication using SQLite.
The Authentication Storage contains three predefined accounts with Argon2 hashed passwords. Users can log in through the POST /login endpoint and receive a signed JWT with their user ID, role and expiration time.
Reservation management, communication between components and the remaining security requirements will be implemented in the next development stages.