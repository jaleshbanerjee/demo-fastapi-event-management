from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class EventCreate(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

class EventOut(EventCreate):
    id: int

    class Config:
        orm_mode = True

class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr

class AttendeeOut(AttendeeCreate):
    id: int

    class Config:
        orm_mode = True

class PaginatedAttendeeOut(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[AttendeeOut]