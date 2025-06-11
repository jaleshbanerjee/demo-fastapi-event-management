from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas import schemas
from crud import crud

router = APIRouter()

# List Events
@router.get("/events", response_model=list[schemas.EventOut], tags=["Event List API"])
async def list_events(db: AsyncSession = Depends(get_db)):
    return await crud.get_events(db)

# Create Events
@router.post("/events", response_model=schemas.EventOut, tags=["Create Event API"])
async def create_event(event: schemas.EventCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_event(db, event)

# Event Attendees List
@router.get("/events/{event_id}/attendees", response_model=schemas.PaginatedAttendeeOut, tags=["Attendees List API"])
async def list_attendees(event_id: int, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_attendees(db, event_id, skip, limit)

# Attendees Registration
@router.post("/events/{event_id}/register", response_model=schemas.AttendeeOut, tags=["Attendees Registration"])
async def register(event_id: int, attendee: schemas.AttendeeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.register_attendee(db, event_id, attendee)
