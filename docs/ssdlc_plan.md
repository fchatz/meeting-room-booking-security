## Secure Software Development Life Cycle Plan

1. **Requirements Phase**


**Activities**:
During the Requirements Phase, I identified the assets that need protection and defined the responsibilities of the three components.
I created the architecture, asset register and access-control matrix to define the system's structure and permissions. 
Additionally, I used the STRIDE threat model to identify possible security threats and their controls. Finally, I selected three secure design principles
to guide the implementation and reduce security risks before coding.


**Security Gate**:
The architecture meets the functional and security requirements.
Component responsibilities and trust boundaries are defined.
Identified threats have appropriate security controls.
If any of these requirements are not satisfied, the design must be revised before proceeding to implementation.

---
2. **Implementation and Build Phase**


**Activities**:
I am planning to implement three components that will run as seperate processes.
Application API will include authentication, user roles and request coordination.
Reservation Service will include reservation management, database access and resource-level authorization.
Scheduling Service will include scheduling validation using the installable helper package.
The security mechanisms will implement authentication, role-based authorization, token validation and reservation ownership checks.
I will use declared dependencies and reproducible builds so the application can be installed and run consistently.

**Security Gate**:
The security gate will ensure that the three components and helper package can be built or installed correctly using their declared dependencies.
Unexpected or unapproved dependencies and build artifacts will be rejected.

---
3. **Testing Phase**


**Activities**:
I am planning to use three categories of tests.
Functional tests: Verify that the Meeting Room Booking System works correctly. Users can create a reservation, retrieve it and cancel it.
authorization tests:  Verify that users and services cannot perform unauthorized operations. For example, Alice cannot cancel Bob's reservation and requests
with invalid tokens are rejected.
Vulnerability investigation and security tests: Plant four vulnerabilities (3 from the course vulnerability catalog and one resulting from component composition). Investigate and document them,
and finally fix confirmed violations of the required security guarantees.
Jenkins will build or validate the three components and perform static code analysis and dependency analysis to identify potential security issues.
Jenkins will run functional and authorization tests automatically in a fresh test environment.
Additionally, the pipeline will fail if confirmed high-severity security vulnerabilities are detected or required authorization tests fail.
Jenkins runs on every push and pull request. Both test and analysis results are saved as artifacts.


**Security Gate**:
The functional and authorization tests should pass.
The confirmed security violations are corrected.
Malformed artifacts are rejected.
If the required tests fail, the pipeline should block the release.

---
4. **Release, Deployment and Operation Phase**


**Activities**:
A production environment would need secure configuration, protection of secret keys and credentials, HTTPS communication between services and security logging.
Additionally, Jenkins will run automated security and functional tests and save their results before a potential production release.

**Security Gate**:
The production release should only be approved if the required tests pass, security findings that block release are resolved and the deployment configuration is secure.


**Example**:

**Asset**: User reservation

**Threat**: Unauthorized cancellation of another user's Reservation

**Requirement/control**: Token validation and reservation ownership verification

**Lifecycle Activity**: Implement authorization checks in the Reservation Service

**Test/Evidence**: Alice attempts to cancel Bob's reservation. Operation rejected

**Gate Decision**: Fail the pipeline if unauthorized cancellation succeeds