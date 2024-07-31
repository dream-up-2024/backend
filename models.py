from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False, default="")
    birth = Column(String(10), nullable=False, default="")
    disabled_type = Column(String(50), nullable=False, default="")
    disabled_level = Column(String(50), nullable=False, default="")
    address = Column(Text, nullable=False, default="")
    issued_date = Column(String(10), nullable=False, default="")
    expiration_period = Column(String(10), nullable=False, default="")
    email = Column(String(50), unique=True, nullable=False)
    signed_date = Column(DateTime, nullable=False, default=datetime.now())
    password = Column(String(100), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 이력서
class UserResume(Base):
    __tablename__ = "user_resume"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(50))
    version = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    content = Column(JSON, nullable=False, default="")


# 자기소개서
class UserCoverLetter(Base):
    __tablename__ = "user_cover_letter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(50))
    type = Column(Integer, nullable=False)   # 지원 동기/성격의 장단점
    version = Column(Integer, nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    content = Column(JSON, nullable=False, default="")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    job_type = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    work_experience = Column(String(50), nullable=False)
    education = Column(String(50), nullable=False)
    address1 = Column(Text, nullable=False)
    address2 = Column(Text, nullable=False)
    working_hour = Column(String(50), nullable=False)
    deadline = Column(String(50), nullable=False)


# class Notice(Base):
#     __tablename__ = "before_notices"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     office = Column(String(100), nullable=False)
#     title = Column(Text, nullable=False)
#     url = Column(Text, nullable=False)
#     description = Column(Text, nullable=False)
#     career = Column(String(50), nullable=False)
#     education = Column(String(50), nullable=False)
#     address = Column(Text, nullable=False)
#     register = Column(String(50), nullable=False)
#     deadline = Column(String(50), nullable=False)
#     contract = Column(Text, nullable=False)
#     working_day = Column(String(50), nullable=False)
#     work_week = Column(String(50), nullable=False, default = '')
