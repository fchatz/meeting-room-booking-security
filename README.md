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
	pwdlib (Argon 2 password hashing)
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

Initialize the Reservation Database:

.\.venv\Scripts\python.exe reservation_service\init_reservation_db.py

This creates the reservations table and a unique index to prevent duplicate active bookings for the same room, date and starting time.

Running the application

Before starting the Application API, configure the JWT signing key in Terminal 1:

$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"

This command generates a random JWT secret key and stores it as an environment variable in Terminal 1. To diplay the generated key so it can be copied to Terminal 2, run:

$env:JWT_SECRET_KEY

The same secret key must be used by both the Application API and the Reservation Service.

The three components run as separate processes. Open three terminals in the project root directory and execute the following commands.
	Application API - Terminal 1
	.\.venv\Scripts\python.exe -m uvicorn application_api.main:app --reload --host 127.0.0.1 --port 8000
	
	Reservation Service - Terminal 2
	Before starting the Reservation Service, set the JWT_SECRET_KEY environment variable using the same key generated in Terminal 1:
	$env:JWT_SECRET_KEY = "<paste the key from Terminal 1>"
	The Reservation service uses this key to verify JWT tokens issued by the Application API. Do not generate a new key in Terminal 2. Then run this command to start Reservation Service:
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

The Reservation Service tests verify successful reservation creation, prevention of duplicates and overlapping bookings, rejection of missing or invalid JWTs, invalid schedules and Scheduling Service unavailability.

The reservation retrieval tests verify that users can access their own reservations, cannot access other users reservations and that administrators can access any reservation. They also verify the 401 and 404 responses. Currently all 18 automated tests pass.

The reservation cancellation tests verify that users can cancel their own reservations, unauthorized users cannot canacel other users reservations and administrators also canacel any reservation.
They also verify that cancelled reservations are marked as cancelled in the database, repeated cancellation attemps are rejected and invalid requests return HTTP errors. Currently all 20 automated tests pass.

The reservation rescheduling tests verify successful rescheduling, ownership restrictions, administrator permissions, prevention of overlapping bookins and rejection of changes to cancelled reservations.
They also verify invalid schedules, nonexistent reservations and JWT authentication. Currently all 22 automated tests pass.

Current Progress

The project is currently under development.

The three independent FastAPI components have been created and tested using their health check endpoints

The Scheduling Service now validates booking dates and times according to the predefined rules. It also uses a separately installable  helper package to calculate reservation ending times.

The Scheduling Service provides a POST /validate endpoint and has automated tests using pytest.

The Application API now supports user authentication using SQLite.
The Authentication Storage contains three predefined accounts with Argon2 hashed passwords. Users can log in through the POST /login endpoint and receive a signed JWT with their user ID, role and expiration time.
The Reservation Service now supports creating reservations through POST /reservations. Booking requests require JWT authentication and are validated by the Scheduling Service. The Reservation Service also checks for overlapping reservations and prevents double booking using database transactions.
The Reservation Service also supports retrieval reservations through GET /reservations/. Authenticated users can retrieve their own reservations, while administrators can retrieve any reservation. The service enforces ownershop checks and returns appropiate HTTP status codes.
The Reservation Service now supports cancelling reservations through DELETE /reservations/. Authenticated users can cancel their own reservations, while administrators can cancel reservations belonging to other users. Cancelled reservations are not deleted from the database, instead their status change from active to cancelled.
The Reservation Service now supports rescheduling through PUT /reservations/. Users can reschedule their own reservations, while administrators can reschedule reservations belonging to other users. The Scheduling Service validates the requested date and time, and the Reservation Service uses database transactions to prevent conflicts and ensure that unsuccessful reschedulling attemps do not modify existing reservations.
Automated tests have been added to verify reservation creation, authentication checks, scheduling failures, reservations retrieval and reservation rescheduling.
Coordination through the Application API and the remaining security requirements will be implemented in the next development stages.