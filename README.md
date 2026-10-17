**Project Description**

This project is a Meeting Room Booking System developed for Software Security Assignment 1.
The application allows users to book meeting rooms, view their reservations, cancel them and reschedule them. Normal users can manage their own reservations,
while administrators have additional permissions to manage reservations belonging to other users.
The system contains three meeting rooms. Bookings are allowed on weekdays from 09:00 to 17:00, and each reservation lasts exactly one hour.
The main goal of this project is to implement a functional application while focusing on secure software development, authentication, authorization and security between different components.

**Architecture**

The application consists of three independent components that communicate through HTTP APIs using JSON.

Application API (port 8000): Handles user authentication, user roles and coordinates requests between the services.
Reservation Service (port 8001): Manages reservations, checks room availability and verifies that users have permissions to access or modify reservations. It is the only service with direct access to the Reservation Database.
Scheduling Service (port 8002): Validates booking dates, times and duration based on predefined scheduling rules. It uses a separately installable helper package.

The application uses SQLite for data storage and JWT tokens for authentication between requests.

More information about the system design and security decisions can be found in the docs/ folder.

**Technologies**
* Python 3.14.7
* FastAPI
* SQLite
* HTTP/JSON
* Pytest
* PyJWT
* pwdlib (Argon 2 password hashing)
* Jenkins
* Bandit
* pip-audit

**Installation**

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
Passwords are stored as Argon2 hashes.

Initialize the Reservation Database:

	.\.venv\Scripts\python.exe reservation_service\init_reservation_db.py

This creates the reservations table and a unique index to prevent duplicate active bookings for the same room, date and starting time.

**Running the application**

Before starting the Application API, configure the JWT signing key in Terminal 1:

	$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"

This command generates a random JWT secret key and stores it as an environment variable in Terminal 1. To display the generated key so it can be copied to Terminal 2, run:

	$env:JWT_SECRET_KEY

The same secret key must be used by both the Application API and the Reservation Service.

The three components run as separate processes. Open three terminals in the project root directory and execute the following commands.

**Application API - Terminal 1**

	.\.venv\Scripts\python.exe -m uvicorn application_api.main:app --reload --host 127.0.0.1 --port 8000
	
**Reservation Service - Terminal 2**

Before starting the Reservation Service, set the JWT_SECRET_KEY environment variable using the same key generated in Terminal 1:

	$env:JWT_SECRET_KEY = "<paste the key from Terminal 1>"
The Reservation service uses this key to verify JWT tokens issued by the Application API. Do not generate a new key in Terminal 2. Then run this command to start Reservation Service:

	.\.venv\Scripts\python.exe -m uvicorn reservation_service.main:app --reload --host 127.0.0.1 --port 8001
	
**Scheduling Service - Terminal 3**

	.\.venv\Scripts\python.exe -m uvicorn scheduling_service.main:app --reload --host 127.0.0.1 --port 8002
	
To verify that the components are running, open the following URLs:

	Application API: http://127.0.0.1:8000/health
	Reservation Service: http://127.0.0.1:8001/health
	Scheduling Service: http://127.0.0.1:8002/health

Each endpoint should return {"status": "ok"}.

Authenticated reservation requests require an Authorization header containing "Bearer" followed by the access token returned from POST /login. The SwaggerUI configuration
does not correctly forward this header from its ordinary header input. For manual authenticated testing, PowerShell can be used to explicity include the Authorization header.

**Testing**

The project uses pytest for automated testing.
To run the test, execute the following command from the project root:

	.\.venv\Scripts\python.exe -m pytest tests/ -v

The current tests cover scheduling validation, working hours, date and time validation, the helper package, the Scheduling Service API and user authentication.
Authentication tests verify successful login, incorrect passwords and unknown users.

The Reservation Service tests verify successful reservation creation, prevention of duplicates and overlapping bookings, rejection of missing or invalid JWTs, invalid schedules and Scheduling Service unavailability.

The reservation retrieval tests verify that users can access their own reservations, cannot access other users reservations and that administrators can access any reservation. They also verify the 401 and 404 responses.

The reservation cancellation tests verify that users can cancel their own reservations, unauthorized users cannot cancel other users reservations and administrators also cancel any reservation.
They also verify that cancelled reservations are marked as cancelled in the database, repeated cancellation attempts are rejected and invalid requests return HTTP errors.

The reservation rescheduling tests verify successful rescheduling, ownership restrictions, administrator permissions, prevention of overlapping bookings and rejection of changes to cancelled reservations.
They also verify invalid schedules, nonexistent reservations and JWT authentication.

The Application API coordination tests verify that reservation creation, retrieval, cancellation and rescheduling requests are correctly forwarded to the Reservation Service.
They also verify that HTTP responses and error codes are preserved and that service unavailability is handled properly. Currently all 36 automated tests pass.

The security regression tests verify that the four vulnerabilities investigated during development have been fixed. These tests cover missing authorization, improper input validation, SQL injection and the JWT trust-boundary vulnerability between the Application API and the Reservation Service.

**Continuous Integration - Jenkins**

The project uses Jenkins for continuous integration. The pipeline is defined in the Jenkinsfile located in the root directory of the repository. Jenkins is configured as a Multibranch Pipeline connected to the GitHub repository.
The pipeline creates a fresh Python virtual environment, installs the project dependencies and initializes the Authentication Storage for testing. It then runs all 36 automated tests using pytest.
Static security analysis is performed using Bandit, which scans the Python source code of the three services and the scheduling helper package. The pipeline fails if Bandit detects medium or high severity security findings. Low severity findings are recorded without blocking the build. The current scan reports one low severity false positive because Bandit identifies the standard JWT token type "bearer" as a possible hardcoded password.
Dependency analysis is performed using pip-audit, which checks installed third-party dependencies for known vulnerabilities. If a known vulnerability is detected, the dependency analysis stage fails.
Jenkins publishes the pytest results using JUnit XML and archives three reports as build artifacts:
* 	pytest-results.xml - Automated test results.
* 	bandit-results.json - Static security analysis findings.
* 	pip-audit-results.json - Dependency vulnerability analysis results.

Jenkins also reports build statuses to GitHub. The Jenkins server runs locally on Windows using the Jenkins WAR file. Jenkins periodically scans the repository (every 15 minutes) to discover branch and pull-request changes. This allows automatic builds of detected changes, although individual builds for every push are not guaranteed.

**Manual Integration Testing**

Manual end-to-end testing was performed with all three services running. Alice successfully logged in through the Application API, created a reservation, retrieved it, rescheduled it and cancelled it using HTTP requests through port 8000.
A final GET request confirmed that the cancelled reservation remained in the database with its status set to "cancelled". This verified communication between the Application API, Reservation Service, Scheduling Service and database.

**Security Investigations**

During development, four vulnerabilities were intentionally introduced and investigated. Three vulnerabilities were selected from the course vulnerability catalog, while the fourth vulnerability resulted from the interaction between different components of the system.

1. CWE-862 - Missing Authorization
	An authorization check was missing in the Reservation Service, allowing unauthorized operation. The vulnerability was investigated and fixed by enforcing the required authorization check.

2. CWE-20 - Improper Input Validation
	The application did not properly validate certain inputs, allowing invalid input to be accepted. The vulnerability was investigated and fixed by improving input validation.

3. CWE-89 - SQL Injection
	A SQL query did not handle user-controlled input securely, making it vulnerable to SQL injection. The vulnerability was investigated and fixed by using secure SQL query handling.

4. Component Composition - JWT Trust-Boundary Vulnerability
	The Reservation Service was modified to skip JWT signature verification, while the Application API forwarded the client's Authorization header. This allowed an attacker to use a forged administrator token to perform an unauthorized operation. The vulnerability was fixed by restoring JWT signature verification in the Reservation Service.

All four vulnerabilities have been fixed and verified using automated security tests. The Git history preserves the vulnerable versions, the fixes and the test evidence for each investigation.

**Remaining Work**

The application functionality, all four vulnerability investigations and the Jenkins CI pipeline have been completed. The remaining work consists of reviewing the final project documentation and preparing the security report with references to the vulnerability investigations, Git commits, automated tests and Jenkins build evidence.