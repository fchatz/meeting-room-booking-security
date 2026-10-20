## Spoofing

| Field             | Description |
|-------------------|--|
| Thread ID         | S1 |
| Trust boundary    | Trust boundary 1 |
| Threat            | Credential theft, password guessing, stolen/forged tokens |
| Affected assets   | Authentication credentials, user sessions |
| Security property | Confidentiality, Integrity |
| Potential impact  | Unauthorized account access, unauthorized modification of their reservations |
| Mitigations       | HTTPS, JWT validation, rate limiting, short token expiration times |
| Planned Test      | Authentication test, invalid token test, rate-limit test |


## Tampering

| Field | Description |
|-----------|-------------|
| Thread ID         |T1 |
| Trust boundary | Trust boundary 1 with authorization enforced across trust boundary 2|
| Threat |Alice manipulates a reservation ID to modify Bob's booking |
| Affected assets |  Reservation records|
| Security property | Integrity |
| Potential impact | Unauthorized modification of another user's reservation records |
| Mitigations | Resource-level authorization and ownership checks |
| Planned Test | Attempt unauthorized modification and verify rejection and unchanged data |




## Repudiation

| Field | Description |
|-----------|-------------|
| Thread ID         | R1|
| Trust boundary |Trust boundary 2 - API to Reservation Service |
| Threat |Administrator denies cancelling another user's reservation |
| Affected assets | Reservation Records, Audit logs |
| Security property | Integrity |
| Potential impact | Inability to determine who performed an action |
| Mitigations | Protected server-side audit logging |
| Planned Test | Perform cancellation and verify the corresponding audit record |


## Information Disclosure

| Field |        Description                                   |
|-----------|-------------------------------------------|
| Thread ID         | I1                                        |
| Trust boundary | Trust boundaries 1 and Trust boundaries 2 |
| Threat | Alice attempts to access Bob's private reservation information                                          |
| Affected assets |         Reservation Records                                  |
| Security property |           Confidentiality                                |
| Potential impact |                  Exposure of private reservation information to unauthorized users                         |
| Mitigations |       Resource-level authorization and ownership checks                                    |
| Planned Test |      Attempt to access another user's reservation and verify rejection                                     |


## Denial of Service

| Field | Description |
|-----------|-------------|
| Thread ID         | D1|
| Trust boundary | Trust boundaries 1 - USER to Application API|
| Threat | Excessive API requests exhaust application resources|
| Affected assets | Application and Service Availability |
| Security property | Availability |
| Potential impact |Legitimate users cannot access the application or experience delays and timesouts
| Mitigations | Rate limiting and optional IP-based restrictions |
| Planned Test | Generate excessive requests and verify throttling |


## Elevation of Privilege

| Field | Description |
|-----------|-------------|
| Thread ID         |E1 |
| Trust boundary | Trust boundary 2 - Application API to Reservation service|
| Threat | Alice manipulates role information to impersonate an administrator|
| Affected assets | User Roles and Permissions, Reservation Records |
| Security property | Integrity |
| Potential impact | A normal user gains administrator privileges |
| Mitigations | Trusted role claims, token verification, server-side authorization |
| Planned Test | Attempt an administrator only action as a normal user using a manipulated role field |


## Tampering

| Field | Description                                                                                                                                                           |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Thread ID         | T2                                                                                                                                                                    |
| Trust boundary | Trust boundary 3 - Reservation Service to Reservation Database                                                                                                        |
| Threat | An attacker exploits an SQL Injection vulnerability to the Reservation Service to manipulate database operations and modify reservation records without authorization |
| Affected assets | Reservation Records                                                                                                                                                   |
| Security property | Integrity                                                                                                                                                             |
| Potential impact | Unauthorized modification or deletion of reservations                                                                                                                 |
| Mitigations | Parameterized SQL queries, input validation, restricted database permissions and authorization checks                                                                 |
| Planned Test | Submit SQL Injection test inputs to the application and verify they cannot alter the intended SQL query or cause unauthorized modifications to reservation records    |



