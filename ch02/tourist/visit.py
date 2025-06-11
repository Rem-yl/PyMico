from datetime import datetime
from typing import List, Set
from uuid import UUID, uuid1

from fastapi import APIRouter, HTTPException
from login import approved_users
from places import TourBasicInfo, TourPreference, tours
from pydantic import BaseModel

router = APIRouter()

tour_preferences: Set[TourPreference] = set()


class Visit(BaseModel):
    id: UUID
    destination: List[TourBasicInfo]
    last_tour: datetime


class Booking(BaseModel):
    id: UUID
    destination: TourBasicInfo
    booking_date: datetime
    tourist_id: UUID


@router.post("/ch02/tourist/tour/booking/add")
def create_booking(tour: TourBasicInfo, tourist_id: UUID) -> Booking:
    if approved_users.get(tourist_id) is None:
        raise HTTPException(status_code=500, detail="tourist not found.")

    booking = Booking(
        id=uuid1(), destination=tour, booking_date=datetime.now(), tourist_id=tourist_id
    )
    approved_users[tourist_id].tours.append(tour)
    approved_users[tourist_id].booked += 1
    tours[tour.id].isBooked = True
    tours[tour.id].visits += 1

    return booking
