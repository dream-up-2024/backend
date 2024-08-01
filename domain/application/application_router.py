from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from typing import Optional

from models import User
# from domain.user.user_router import get_current_user
from config import settings
from database import SessionLocal, get_db
from domain.application import application_crud, application_schema

import json

router = APIRouter(
    prefix="/api/application",
)

# 이력서 작성
@router.post("/resume/{user_email}", status_code=200)
def resume_create(user_email: str, _resume_create: application_schema.UserResumeCreate, 
                  db: Session = Depends(get_db)):
                #   current_user: User = Depends(get_current_user)):
                # user_email: str = ''):
    application_crud.create_user_resume(db=db, resume_create=_resume_create, user_email=user_email)


# email="ryeonk"
# 자기소개서 작성
@router.post("/cover-letter/{user_email}", status_code=200)
def cover_letter_create(user_email: str, 
                        _cover_letter_create: application_schema.UserCoverLetterCreate, 
                        db: Session = Depends(get_db)):
                        # q: Optional[str] = None):
                        # user_email: str = ''):
    data = application_crud.create_user_cover_letter(db=db, cover_letter_create=_cover_letter_create, user_email=user_email)
    return data


# 이력서 반환
@router.get("/resume/{user_email}", status_code=200)
def resume_get(user_email: str, db: Session = Depends(get_db)):
    data = application_crud.get_user_resume(db=db, user_email=user_email)
    return data


# email="ryeonk"
# 자기소개서 반환
@router.get("/cover-letter/{user_email}", status_code=200)
def cover_letter_get(user_email: str, db: Session = Depends(get_db)):
    data = application_crud.get_user_cover_letter(db=db, user_email=user_email)
    return data


# 지원서 반환
@router.get("/personal/{user_email}", status_code=200)
def cover_letter_get(user_email: str, db: Session = Depends(get_db)):
    # data = application_crud.get_user_cover_letter(db=db, user_email=user_email)
    # return data
    return user_email
