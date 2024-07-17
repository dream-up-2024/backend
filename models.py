from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "uesr"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    name = Column(String(10), nullable=False)


class Members(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    birth = Column(String(10), nullable=False)
    disabled_type = Column(String(50), nullable=False)
    disabled_level = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    issued_date = Column(String(10), nullable=False)
    expiration_period = Column(String(10), nullable=False)
    signed_date = Column(DateTime, default=datetime.now(), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())

