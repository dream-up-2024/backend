from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base


class Users(Base):
    __tablename__ = "uesr"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    name = Column(String(10), nullable=False)
