## Access-Control Matrix

| Operation | Normal User | Administrator |
|-----------|-------------|---------------|
| Book a room | Conditional | Conditional |
| Cancel own reservation | Conditional | Conditional |
| Cancel another user's reservation | Denied | Conditional |
| Reschedule own reservation | Conditional | Conditional |
| Reschedule another user's reservation | Denied | Conditional |
| View own reservation details | Allowed | Allowed |
| View another user's reservation details | Denied | Allowed |

**Conditional means the operation is allowed only when the conditions relevant to the specific operation are satisfied.**



## Conditions for each operation

| Operation | Conditions |
|-----------|-------------|
| Book | The room must be available and the date/time must follow scheduling rules|
| Cancel | The reservation must be active and the user must be its owner or an administrator|
| Reschedule | The reservation must be active and the user must have permissions. Additionally the new slot must be valid and available |



## Service Level Access Control Matrix

| Service | Authentication Storage | Reservation Database |
|-----------|------------------------|----------------------|
| Application API | Read                   | -                    |
| Reservation Service | -                      | Read/Write                    |
| Scheduling Service | -                      | -                    |


The Application API should only read records inside the Authentication Storage to authenticate a user and its role. Should not have permission to write because the application will use predefined seeded users.

The Reservation Service is the only component that have read/write permissions to the Reservation Database as its the only component that check the availability of the rooms and makes new bookings/reschedules/cancelations.

Scheduling Service should not  have access to either Authentication Storage or Reservation Database, as its role is to validate based on predefined rules.

| Source | Destination | Interaction                                                                                 |
|-----------|-------------|---------------------------------------------------------------------------------------------|
| Reservation Service | Scheduling Service | Requests scheduling validation                                                              |
| Application API | Reservation Service | Forwards reservation requests with JWT                                                      |
| Scheduling Service | Reservation Service | NOt used in the intended workflow                                                           |
| User | Reservation Service | Direct requests are possible but protected operations require a valid JWT and authorization |


## Authorization Between Components

The Application API authenticates users based on information stored in Authentication Storage. The plan is to use JWT tokens and HTTPS to secure the communication between the components.

The JWT contains information about the authenticated users, such as their ID and role. When the Application API sends a request to the Reservation Service, the Reservation Service must verify that the token is valid, has not expired and comes from a trusted issuer. HTTPS protects the information while it is being transferred between services. However, a valid JWT does not automatically mean that the user is authorized to perform every operation. For example, if Alice has a valid JWT, the Reservation Service must check if the reservation belongs to Alice before allowing her to cancel it. If the reservation belongs to Bob and Alice is not an administrator, the operation should be denied.

The internal services should not automatically trust each other just because they belong to the same application. Each service must verify the requests it receives and enforce the security checks related to its responsibilities. The Reservation Service must also ensure that booking rules cannot be bypassed by sending requests directly to it.

