from __future__ import annotations

from datetime import datetime
from enum import Enum, IntEnum
from typing import Dict, List
from uuid import UUID, uuid1

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

tours: Dict[UUID, Tour] = {}
tours_basic_info: Dict[UUID, TourBasicInfo] = {}
tours_locations: Dict[UUID, TourLocation] = {}


class StarRating(IntEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class Post(BaseModel):
    feedback: str
    rating: StarRating
    date_posted: datetime


class Location(BaseModel):
    latituede: float
    longitude: float = 0.0


class TourType(str, Enum):
    resort = "resort"
    hotel = "hotel"
    bungalow = "bungalow"
    tent = "tent"
    exclusive = "exclusive"


class AmenitiesTypes(str, Enum):
    restaurant = "restaurant"
    pool = "pool"
    beach = "beach"
    shops = "shops"
    bars = "bars"
    activities = "activities"


class TourInput(BaseModel):
    name: str
    city: str
    country: str
    type: TourType
    location: Location
    amenities: List[AmenitiesTypes]


class Tour(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    type: TourType
    location: Location
    amenities: List[AmenitiesTypes]
    feedbacks: List[Post]
    ratings: float
    visits: int
    isBooked: bool


class TourBasicInfo(BaseModel):
    id: UUID
    name: str
    type: TourType
    amenities: List[AmenitiesTypes]
    ratings: float


class TourLocation(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    location: Location


class TourPreference(str, Enum):
    party = "party"
    extreme = "hiking"
    staycation = "staycation"
    groups = "groups"
    solo = "solo"


@router.put("/ch02/admin/destination/update", status_code=status.HTTP_202_ACCEPTED)
def update_tour_destination(tour: Tour) -> JSONResponse:
    try:
        tid = tour.id
        tours[tid] = tour
        tour_basic_info = TourBasicInfo(
            id=tid,
            name=tour.name,
            type=tour.type,
            amenities=tour.amenities,
            ratings=tour.ratings,
        )
        tour_location = TourLocation(
            id=tid,
            name=tour.name,
            city=tour.city,
            country=tour.country,
            location=tour.location,
        )
        tours_basic_info[tid] = tour_basic_info
        tours_locations[tid] = tour_location

        return JSONResponse(
            content={"message": "tour updated"}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"update tour error: {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/ch02/admin/destination/list", status_code=200)
def list_all_tours() -> Dict[UUID, Tour]:
    return tours


@router.post("/ch01/admin/destination/add")
def add_tour_destination(tour_input: TourInput) -> JSONResponse:
    try:
        tid = uuid1()
        tour = Tour(
            id=tid,
            name=tour_input.name,
            city=tour_input.city,
            country=tour_input.country,
            type=tour_input.type,
            location=tour_input.location,
            amenities=tour_input.amenities,
            feedbacks=[],
            ratings=0.0,
            visits=0,
            isBooked=False,
        )
        tour_basic_info = TourBasicInfo(
            id=tid,
            name=tour_input.name,
            type=tour_input.type,
            amenities=tour_input.amenities,
            ratings=0.0,
        )
        tour_location = TourLocation(
            id=tid,
            name=tour_input.name,
            city=tour_input.city,
            country=tour_input.country,
            location=tour_input.location,
        )

        tours[tid] = tour
        tours_basic_info[tid] = tour_basic_info
        tours_locations[tid] = tour_location
        tour_json = jsonable_encoder(tour)
        return JSONResponse(content=tour_json, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(
            content={"message": f"invalid tour {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
