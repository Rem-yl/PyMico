from datetime import datetime

from database import Base
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=False)
    password = Column(String(50), nullable=False, unique=False, index=False)
    date_approved = Column(
        Date, default=datetime.now(), nullable=False, unique=False, index=False
    )
    usertype = Column(Integer, nullable=False, unique=False, index=False)

    trainers = relationship("Profile_Trainers", back_populates="login", uselist=False)
    members = relationship("Profile_Members", back_populates="login", uselist=False)


class Profile_Trainers(Base):
    __tablename__ = "profile_trainers"

    id = Column(Integer, primary_key=True, index=True)
    login_id = Column(
        Integer, ForeignKey("login.id"), nullable=False, unique=True, index=False
    )
    first_name = Column(String(50), nullable=False, unique=False, index=False)
    last_name = Column(String(50), nullable=False, unique=False, index=False)
    age = Column(Integer, nullable=False, unique=False, index=False)

    login = relationship("Login", back_populates="trainers")


class Profile_Members(Base):
    __tablename__ = "profile_members"

    id = Column(Integer, primary_key=True, index=True)
    login_id = Column(
        Integer, ForeignKey("login.id"), nullable=False, unique=True, index=False
    )
    trainer_id = Column(
        Integer,
        ForeignKey("profile_trainers.id"),
        nullable=True,
        unique=False,
        index=False,
    )
    first_name = Column(String(50), nullable=False, unique=False, index=False)
    last_name = Column(String(50), nullable=False, unique=False, index=False)
    age = Column(Integer, nullable=False, unique=False, index=False)
    height = Column(Float, unique=False, index=False)
    weight = Column(Float, unique=False, index=False)
    membership_type = Column(String(50), unique=False, index=False)

    login = relationship("Login", back_populates="members")
