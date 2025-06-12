

## FastAPI Event Management System ##

This is a simple event management system built using **FastAPI**, **SQLAlchemy (Async)**, and **SQLite**. It allows:

- Creating events
- Registering attendees
- Listing attendees with pagination
- Built with async-ready SQLAlchemy
- Swagger UI for interactive testing

### 1. Setup instructions

### 1.1. Clone the repository
```
git clone https://github.com/jaleshbanerjee/demo-fastapi-event-management.git
cd fastapi_app
```
### 1.2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 1.3. Install dependencies
```
pip install -r requirements.txt
```
### 1.4. Run the app
```
cd event_mgmt\app
uvicorn main:app --reload --port 8000
or,
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
### 2. Assumptions

Here, I'm FastAPI for this project because it offers a modern, high-performance, and developer-friendly framework for building APIs. 

SQLite is used for simplicity (no setup needed).

All event and attendee operations are synchronous in logic but use SQLAlchemy's AsyncSession for future scalability.

No authentication is implemented.

All time fields are handled as strings (ISO format YYYY-MM-DD).

Email uniqueness and event capacity checks are done at registration time.

### 3. Sample API Requests

### 3.1. Create Event
```
curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" -d '{
  "name": "Joy",
  "location": "Bangalore",
  "start_time": "2025-06-20",
  "end_time": "2025-06-20",
  "max_capacity": 100
}'
```
### 3.2. Register Attendee
```
curl -X POST "http://127.0.0.1:9000/events/1/register" -H "Content-Type: application/json" -d '{
  "name": "Joy",
  "email": "joy@example.com"
}'
```
### 3.3. Get Attendees (Paginated)
```
curl -X GET "http://127.0.0.1:9000/events/1/attendees?skip=0&limit=10"
```
### 3.4. You can also test this via the Swagger UI at:
```
http://127.0.0.1:9000/docs
```
You can use Swagger at for testing and exploring endpoints.


### 4. Project Structure
```
event_mgmt/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── crud/
│   │   └── crud.py
│   ├── db/
│   │   └── database.py
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── utils/
│   │   └── timezone.py
│   └── main.py
└── tests
└── README.md
```
### 5.  Database Schema Overview

This application contains two main models (tables):

Event – represents an event.

Attendee – represents a person registered for an event.

These are connected by a one-to-many relationship (one event → many attendees)

### 5.1. Event Table

--------------------------------------------------------------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)

    attendees = relationship("Attendee", back_populates="event")
--------------------------------------------------------------------------

Primary key: id

Fields: name, location, start_time, end_time, max_capacity

Relationship: One event → many attendees (attendees list)

### 5.2. Attendee Table

--------------------------------------------------------------------------
class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="attendees")
--------------------------------------------------------------------------

Primary key: id

Fields: name, email, event_id (foreign key)

Relationship: Many attendees → one event

### 5.3. Relationship Summary

One Event has many Attendees.

Each Attendee belongs to one Event.

### 6. TODO / Future Improvements

Add authentication & authorization

Add filtering for events/attendees

Add support for time zones and datetime validations

Switch to PostgreSQL or MySQL for production


