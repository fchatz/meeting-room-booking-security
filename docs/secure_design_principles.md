## Least Privilege

**Design Decision**:

The Application API should only read Authentication Storage and cannot access Reservation Database directly because the database is handled only by Reservation Service.
Scheduling Service receives only the information needed to validate scheduling operations, to avoid exposing unnecessary reservation or user data. Ordinary users can only modify their own reservations, while administrators
have explicity assigned additional permissions.

**Planned Implementation**:

The restrictions will be enforced by using role-based authorization for ordinary users and administrators, reservation ownership verification before allowing modifications.
Additionally, the direct database access will be restricted only to the Reservation Service who is responsible for the database.
Permissions will be enforced by the relevant services rather than relying only on the client or frontend.


**Planned Test/Evidence**:

The test will include Alice and Bob as ordinary users. Alice will attempt to cancel Bob's reservation using his reservation ID.
The expected result should be that the Reservation Service rejects the unauthorized operation and Bob's reservation remains unchanged.

---

## Complete Mediation

**Design Decision**:

Authentication performed by the Application API is not sufficient to authorize access to reservations. A user could bypass the Application API and send requests directly to the Reservation Service. For this reason, the Reservation Service should independently verify JWT tokens and enforce authorization checks whenever a protected reservation operation is requested.

**Planned Implementation**:

The Application API will authenticate users and generate signed JWT tokens containing their identity and role. The Reservation Service will independently verify the token's signature, expiration, issuer and audience using an established library. It will also check the user's permissions and reservation ownership before performing protected operations.


**Planned Test/Evidence**:

The test will include Alice and Bob as ordinary users. Alice will attempt to cancel Bob's reservation using his reservation ID and bypassing Application API.
She will send the request to the Reservation Service.
The expected result should be that the Reservation Service rejects the unauthorized operation and Bob's reservation remains unchanged.

---
## Fail-Safe Defaults

**Design Decision**:

If the Application API or the Reservation Service cannot verify that an operation is authorized then it should immediately stop.

**Planned Implementation**:

The application should not trust unverified data. The requests are denied when required authorization information is missing or invalid.
Unknown roles receive no permissions automatically.
A database failure during authorization prevents the protected operation from proceeding.

**Planned Test/Evidence**:

The test will demonstrate that a request with an invalid token or missing role will automatically reject the request rather than unauthorized access.