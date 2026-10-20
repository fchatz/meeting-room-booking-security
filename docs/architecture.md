## Meeting Room Booking System Architecture

**Overview**

The Meeting Room Booking System is an application where users can book, cancel, and reschedule meeting rooms inside a building. The system has three meeting rooms, and the available booking hours are from 09:00 to 17:00 on weekdays. Each booking lasts exactly one hour.
To book a room, users must choose their preferred date, time and meeting room. If the selected room is available, the reservation can be created. The same process applies when rescheduling a reservation, where users can select a new date, time, or room.
To cancel a reservation, there is no need for an availability check. The user only need to have an active reservation under their name. Instead of deleting the reservation from the database, the status changes from active to cancelled.

**Users and Permissions**

The application has two types of users:

Normal users: Can book meeting rooms and cancel or reschedule reservations that belong to them.

Administrators: Can perform the same operations as normal users, but they can also cancel or reschedule reservations belonging to other users.

For testing purposes, the system will have at least two normal user accounts and one administrator account.

**System Architecture**

I designed the application around three independent components to separate their responsibilities and improve the security system. Each component will run as a separate process and communicate with the others through APIs.

Application API: This component receives requests from users and handles authentication. It communicates with the authentication storage to verify the user's identity. After authentication, the Application API forwards reservation requests to the Reservation Service. The Reservation Service communicates with the Scheduling Service when scheduling validation is required.

Reservation Service: This component is responsible for managing reservations and communicating with the reservation database. It checks whether a requested room is already booked and verifies whether the user has permission to perform the requested operation. It is also responsible for preventing two users from booking the same room at the same time.

Scheduling Service: This component validates the scheduling information received from the Reservation Service. For example, it checks whether the selected date is a weekday, whether the time is within the allowed booking hours, and whether the reservation duration is valid. It uses a separate helper package for date and time calculations. The Scheduling Service does not need direct access to the reservation database.

By separating these responsibilities, each component only needs access to the information required for its operations.

**Data Storage**

The application uses two types of storage:

Authentication Storage: Contains the seeded user accounts and the information needed for authentication and identifying user roles.

Reservation Database: Contains the reservations created by users. Each reservation includes a reservation ID, user ID, room ID, date, time and status

Only the Reservation Service has direct access to the reservation database. The other components must communicate with it through its API when reservation information is needed.

**Data flow**

The workflow for creating a reservation is the following:

Alice wants to book meeting room 2 on Monday, October 12, from 10:00 to 11:00.

First Alice logs in through the Application API using her username and password. After successful authentication, the Application API generates a signed JWT and returns it to Alice.

Alice then sends a booking request to the Application API, including the selected room, date, time and her JWT.

The Application API forwards the request to the Reservation Service.

The Reservation Service verifies the JWT and requests scheduling validation from the Scheduling Service.

The Reservation Service verifies the required permissions and checks the database to see if the room is already reserved for that time. The availability check and reservation creation must be handled atomically to prevent race conditions when multiple users try to book the same room.

If all conditions are satisfied, the reservation is stored in the database, and the result is returned to Alice through the Application API.

**Trust Boundaries**

The architecture contains three main trust boundaries.

Trust boundary 1: Separates the user from the Application API and Authentication Storage. Requests coming from users cannot be trusted, so the Application API must authenticate users and validate their requests.

Trust boundary 2: Separates the Application API from the Reservation Service and Scheduling Service. Even though these components belong to the same application, they should not automatically trust each other. Each service must enforce the security checks relevant to its responsibilities.

Trust boundary 3: Separates the Reservation Service from the reservation database. Only the Reservation Service should have permission to access and modify reservation records. This helps prevent other components from directly accessing protected data.



