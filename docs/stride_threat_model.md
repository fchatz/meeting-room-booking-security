Spoofing



Threat ID: S1

Trust boundary: Trust boundary 1

Threat: Credential theft, password guessing, stolen/forged tokens

Affected assets: Authentication credentials, user sessions

Security property: Confidentiality, Integrity

Potential impact: Unauthorized account access, unauthorized modification of their reservations

Mitigations: HTTPS, JWT validation, rate limiting, short token expiration times

Planned Test: Authentication test, invalid token test, rate-limit test





Tampering



Threat ID: T1

Trust boundary: Trust boundary 1 with authorization enforced across trust boundary 2

Threat: Alice manipulates a reservation ID to modify Bob's booking

Affected asset: Reservation records

Security property: Integrity

Potential Impact: Unauthorized modification of another user's reservation records

Mitigation: Resource-level authorization and ownership checks

Planned Test: Attempt unauthorized modification and verify rejection and unchanged data





Repudiation



Threat ID: R1

Trust boundary: Trust boundary 2 - API to Reservation Service

Threat: Administrator denies cancelling another user's reservation

Affected assets: Reservation Records, Audit logs

Security Property: Integrity

Potential Impact: Inability to determine who performed an action

Mitigation: Protected server-side audit logging

Planned Test: Perform cancellation and verify the corresponding audit record





Information Disclosure



Threat ID: I1

Trust boundaries: Trust boundaries 1 and Trust boundaries 2

Threat: Alice attempts to access Bob's private reservation information

Affected asset: Reservation Records

Security property: Confidentiality 

Potential Impact: Exposure of private reservation information to unauthorized users

Mitigation: Resource-level authorization and ownership checks

Planned Test: Attempt to access another user's reservation and verify rejection





Denial of Service



Threat ID: D1

Trust boundary: Trust boundaries 1 - USER to Application API

Threat: Excessive API requests exhaust application resources

Affected asset: Application and Service Availability 

Security property: Availability

Potential Impact: Legitimate users cannot access the application or experience delays and timesouts

Mitigation: Rate limiting and optional IP-based restrictions

Planned Test: Generate excessive requests and verify throttling 





Elevation of Privilege



Threat ID: E1

Trust boundary: Trust boundary 2 - Application API to Reservation service

Threat: Alice manipulates role information to impersonate an administrator

Affected assets: User Roles and Permissions, Reservation Records

Security property: Integrity

Potential Impact: A normal user gains administrator privileges

Mitigation: Trusted role claims, token verification, server-side authorization

Planned Test: Attempt an administrator only action as a normal user using a manipulated role field





Tampering



Threat ID: T2

Trust boundary: Trust boundary 3 - Reservation Service to Reservation Database

Threat: An attacker exploits an SQL Injection vulnerability to the Reservation Service to manipulate database operations and modify reservation records without authorization

Affected assets: Reservation Records

Security property: Integrity

Potential Impact: Unauthorized modification or deletion of reservations

Mitigation: Parameterized SQL queries, input validation, restricted database permissions and authorization checks

Planned Test: Submit SQL Injection test inputs to the application and verify they cannot alter the intended SQL query or cause unauthorized modifications to reservation records







