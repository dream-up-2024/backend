from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class MemberCreate(BaseModel):
    name: str
    birth: str
    disabled_type: str
    disabled_level: str
    address: str
    issued_date: str
    expiration_period: str
    email: EmailStr
    password1: str
    password2: str

    @field_validator('name', 'email', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str