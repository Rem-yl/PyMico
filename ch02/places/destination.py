from __future__ import annotations

from datetime import datetime
from enum import Enum, IntEnum
from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter
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
