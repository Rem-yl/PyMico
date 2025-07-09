from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class Gender(IntEnum):
    MELE = 0
    FEMELE = 1


class MemberLevel(IntEnum):
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4


class UserType(IntEnum):
    MEMBER = 0
    TRAINER = 1


class UserReq(BaseModel):
    username: str
    password: str


class SignUpReq(BaseModel):
    username: str
    password: str
    usertype: UserType

    class Config:
        from_attributes = True


class SignUpOut(BaseModel):
    id: int
    username: str
    user_type: UserType
    date_approved: datetime

    class Config:
        from_attributes = True


class MemberReq(BaseModel):
    signup_id: int

    age: int
    level: MemberLevel
    gender: Gender


class MemberOut(BaseModel):
    id: int
    signup: SignUpOut
    age: int
    level: MemberLevel
    gender: Gender

    class Config:
        from_attributes = True


class TrainerReq(BaseModel):
    signup_id: int

    age: int
    level: MemberLevel
    gender: Gender
    height: float
    weight: float

    class Config:
        from_attributes = True
