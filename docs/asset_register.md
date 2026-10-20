**Asset**: Authentication Credentials and password hashes.

**Description**: The Authentication Storage contains user authentication information, such as usernames and password hashes. The Application API uses this information to verify users when they log in.

**Owner**: Application API.

**Security requirements**: Confidentiality, Integrity, Availability.

---

**Asset**: Reservation Records.

**Description**: The Reservation Records contain information about the reservations and these records are used for the bookings. The application uses these records to manage reservations and determine room availability.

**Owner**: Reservation Service.

**Security requirements**: Confidentiality, Integrity, Availability.

---

**Asset**: User roles and permissions.

**Description**: The Authentication Storage contains information about each user's assigned role. The Application API issues JWTs containing roles, while the Reservation Service enforces reservation permissions.

**Owner**: Application API.

**Security requirements**: Confidentiality, Integrity.

---

**Asset**: Scheduling rules and configuration.

**Description**: The Scheduling Service uses predefined booking rules such as available weekdays, working hours and reservation duration. The application uses these rules to validate the booking requests.

**Owner**: Scheduling Service.

**Security requirements**: Integrity.

---

**Asset**: Audit Logs.

**Description**: Records of important actions performed by users and administrators.

**Owner**: Reservation Service.

**Security requirements**: Confidentiality, Integrity, Availability.

---

**Asset**: Authentication Tokens/Sessions.

**Description**: Information used to identify authenticated users across requests.

**Owner**: Application API, Authentication subsystem.

**Security requirements**: Confidentiality, Integrity.

---

**Asset**: Application and Service Availability.

**Description**: The ability of our three components to process legitimate requests.

**Owner**: Application API, Reservation Service, Scheduling Service.

**Security requirements**: Availability.



