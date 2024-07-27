from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Any, Dict


class UserResumeCreate(BaseModel):
    email: str
    content: Dict[str, Any]