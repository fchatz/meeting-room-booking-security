Least Privilege

Design Decision:

The Application API should only read Authentication Storage and cannot access Reservation Database directly because the database is handled only by Reservation Service.
Scheduling Service receives only the information needed to validate scheduling operations, to avoid exposing unnecessary reservation or user data. Ordinary users can only modify their own reservations, while administrators
have explicity assigned additional permissions.


Planned Implementation:

The restrictions will be enforced by using role-based authorization for ordianry users and administrators, reservation ownership verification before allowing modifications.
Additionally, the direct database access will be restricted only to the Reservation Service who is responsible for the database.
Permissions will be enforced by the relevant services rather than relying only on the client or frontend.


Planned Test/Evidence:

The test will include Alice and Bob as ordinary users. Alice will attempt to cancel Bob's reservation using his reservation ID.
The expected result should be that the Reservation Service rejects the unauthorized operation and Bob's reservation remains unchanged.


Complete Mediation

Design Decision:

Both the Application API and Reservation Service should verify authorization. If only Application API did authorization verification once upon login, the user 
could send unauthorized requests after verification. Additionally, a user could skip Application API and send request directly to Reservation Service.
That's why both the Application API and the Reservation Service should verify authorization.

Planned Implementation:

Both Application API and Reservation Service will have authorization checks.
Implementation will include token verification using established library.
The Reservation Service will validate the token's signature, expiration and intended audience and check the user's permission and ownership of the requested reservation 
before performing the operation.


Planned Test/Evidence:

The test will include Alice and Bob as ordinary users. Alice will attempt to cancel Bob's reservation using his reservation ID and bypassing Application API.
She will send the request to the Reservation Service.
The expected result should be that the Reservation Service rejects the unauthorized operation and Bob's reservation remains unchanged.


Fail-Safe Defaults

Design Decision:

If the Application API or the Reservation Service cannot verify that an operation is authorized then it should immediately stop.

Planned Implementation:

The application should not trust unverified data. The requests are denied when required authorization information is missing or invalid.
Unknown roles receive no permissions automatically.
A database failure during authorization prevents the protected operation from proceeding.


Planned Test/Evidence:

The test will demonstrate that a request with an invalid token or missing role will automatically reject the request rather than unauthorized access.