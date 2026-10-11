Asset: Authentication Credentials and password hashes.

Description: The Authentication Storage contains user authentication information, such as usernames and password hashes. The Application API uses this information to verify users when they log in.

Owner: Application API.

Security requirements: Confidentiality, Integrity, Availability.





Asset: Reservation Records.

Description: The Reservation Records contain information about the reservations and these records are used for the bookings. The application uses these records to manage reservations and determine room availability.

Owner: Reservation Service.

Security requirements: Confidentiality, Integrity, Availability.





Asset: User roles and permissions.

Description: The Application API contains information about each user's assigned roles. The application uses this information to determine which operations a user is allowed to perform.

Owner: Application API.

Security requirements: Confidentiality, Integrity.





Asset: Scheduling rules and configuration.

Description: The Scheduling Service uses predefined booking rules such as available weekdays, working hours and reservation duration. The application uses these rules to validate the booking requests.

Owner: Scheduling Service.

Security requirements: Integrity.



