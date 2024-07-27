from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    birth = Column(String(10), nullable=False)
    disabled_type = Column(String(50), nullable=False)
    disabled_level = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    issued_date = Column(String(10), nullable=False)
    expriration_period = Column(String(10), nullable=False)
    signed_date = Column(DateTime, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    updated_date = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    office = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    career = Column(String(50), nullable=False)
    education = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    register = Column(String(50), nullable=False)
    deadline = Column(String(50), nullable=False)
    contract = Column(Text, nullable=False)
    working_day = Column(String(50), nullable=False)
    work_week = Column(String(50), nullable=False, default = '')
