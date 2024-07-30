from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Any, Dict


class UserResumeCreate(BaseModel):
    content: Dict[str, Any]


class UserCoverLetterCreate(BaseModel):
    type: str
    content: Dict[str, Any]

    class Config:
        orm_mode = True