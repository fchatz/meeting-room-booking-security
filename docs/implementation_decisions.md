**Programming language**

I selected python because of its simplicity and of the large ecosystem of existing libraries.

---
**Framework**

I selected FastAPI as my framework because of its high-performace with Python and its ideal for building fast, reliable RESTful APIs and microservices.

---
**Database**

I selected SQLite because of the serverless database engine to store the records, zero configuration and simple deployment.
The only service that will have access to the database is the Reservation Service.

---
**Component Communication**

I will use HTTP/JSON for the components communication.
The components run as separate processes on different ports.
This allows each component to be developed and tested independently.