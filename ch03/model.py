from uuid import UUID

from pydantic import BaseModel


class Book(BaseModel):
    id: UUID
    title: str
    author: str


class User(BaseModel):
    id: UUID
    username: str
    password: str


class UserOut(BaseModel):
    id: UUID
    username: str
