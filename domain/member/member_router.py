from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal, get_db
from domain.member import member_crud, member_schema
from domain.member.member_crud import pwd_context

from config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

router = APIRouter(
    prefix="/api/member",
)

@router.post("/craete", status_code=status.HTTP_204_NO_CONTENT)
def member_create(_member_create: member_schema.MemberCreate, db: Session = Depends(get_db)):
    member = member_crud.get_existing_member(db, member_create=_member_create)
    if member:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    member_crud.create_member(db=db, member_create=_member_create)

@router.post("/login", response_model=member_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    member = member_crud.get_member(db, form_data.username)
    if not member or not pwd_context.verify(form_data.password, member.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": member.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": member.email
    }