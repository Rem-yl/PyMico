from datetime import datetime

from database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SignUp(Base):
    __tablename__ = "signup"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=False, index=False)
    password = Column(String(50), unique=False, index=False)
    user_type = Column(
        Integer, unique=False, index=False
    )  # 0 for member, 1 for trainer
    date_approved = Column(DateTime, default=datetime.now)

    trainers = relationship(
        "Trainer", back_populates="signup", uselist=False, cascade="all, delete"
    )
    members = relationship(
        "Member", back_populates="signup", uselist=False, cascade="all, delete"
    )


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=False, index=False)
    password = Column(String(50), unique=False, index=False)
    login_time = Column(DateTime, default=datetime.now)
    user_type = Column(
        Integer, unique=False, index=False
    )  # 0 for member, 1 for trainer


class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    signup_id = Column(
        Integer,
        ForeignKey("signup.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    age = Column(Integer, unique=False, index=False)
    level = Column(Integer, unique=False, index=False)
    gender = Column(Integer, unique=False, index=False)
    height = Column(Float, unique=False, index=False)
    weight = Column(Float, unique=False, index=False)

    signup = relationship("SignUp", back_populates="trainers", uselist=False)
    members = relationship("Member", back_populates="trainer")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    signup_id = Column(
        Integer,
        ForeignKey("signup.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    trainer_id = Column(
        Integer, ForeignKey("trainers.id"), unique=False, nullable=True, index=False
    )

    age = Column(Integer, unique=False, index=False)
    level = Column(Integer, unique=False, index=False)
    gender = Column(Integer, unique=False, index=False)

    signup = relationship("SignUp", back_populates="members", uselist=False)
    trainer = relationship("Trainer", back_populates="members", uselist=False)
