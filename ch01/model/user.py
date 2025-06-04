from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class ValidUser(BaseModel):
    id: UUID
    username: str
    password: str
    passphrase: str


class UserType(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    ALUMNI = "alumni"
    STUDENT = "student"


class UserProfile(BaseModel):
    firstname: str
    lastname: str
    middle_initial: str
    age: Optional[int] = 0
    salary: Optional[int] = 0
    birthday: date
    user_type: UserType


class PostType(str, Enum):
    INFO = "information"
    INQUIRY = "inquiry"
    QUOTE = "quote"
    TWIT = "twit"


class Post(BaseModel):
    topic: Optional[str] = None
    message: str
    date_posted: datetime


class ForumPost(BaseModel):
    id: UUID
    topic: Optional[str] = None
    message: str
    post_type: PostType
    date_posted: datetime
    username: str


class ForumDiscussion(BaseModel):
    id: UUID
    main_post: ForumPost
    replies: Optional[List[ForumPost]] = None
    author: UserProfile
