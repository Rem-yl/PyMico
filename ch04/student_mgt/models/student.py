from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Signup(BaseModel):
    id: UUID
    username: str
    password: str
    is_admin: bool = False


class SignupReq(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class Login(BaseModel):
    id: UUID
    username: str
    password: str


class StudentReq(BaseModel):
    name: str
    age: int


class Student(BaseModel):
    id: UUID
    name: str
    age: int


class AssignmentRequest(BaseModel):
    bin_id: int
    assgn_id: int
    title: str
    date_completed: Optional[datetime] = None
    date_due: datetime
    rating: Optional[float] = None
    course: str
