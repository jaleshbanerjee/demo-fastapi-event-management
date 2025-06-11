from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from db import models
from schemas import schemas
from sqlalchemy.orm import selectinload 
from sqlalchemy import func

# Get list of All Events from DB
async def get_events(db: AsyncSession):
    result = await db.execute(select(models.Event))
    return result.scalars().all()

# Create a Entry in DB for Event
async def create_event(db: AsyncSession, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event

# Get Attendees List for Event
async def get_attendees(db: AsyncSession, event_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Attendee).where(models.Attendee.event_id == event_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_attendees(db: AsyncSession, event_id: int, skip: int = 0, limit: int = 10):
    # Total number of attendees for the event
    total_result = await db.execute(
        select(func.count()).select_from(models.Attendee).where(models.Attendee.event_id == event_id)
    )
    total = total_result.scalar_one()

    # Paginated result
    result = await db.execute(
        select(models.Attendee).where(models.Attendee.event_id == event_id).offset(skip).limit(limit)
    )
    attendees = result.scalars().all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": attendees
    }

# Register Attendees in DB dor a paricular event
async def register_attendee(db: AsyncSession, event_id: int, attendee: schemas.AttendeeCreate):
    result = await db.execute(
        select(models.Event)
        .options(selectinload(models.Event.attendees))  # <-- Eagerly load attendees
        .filter(models.Event.id == event_id)
    )
    event = result.scalar_one_or_none()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if len(event.attendees) >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event capacity full")

    new_attendee = models.Attendee(
        name=attendee.name,
        email=attendee.email,
        event_id=event.id
    )
    db.add(new_attendee)
    await db.commit()
    await db.refresh(new_attendee)
    return new_attendee


