from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from database import SessionLocal, get_db
from domain.notice import notice_crud, notice_schema

router = APIRouter(
    prefix="/api/notice",
)

@router.get("", status_code=200)
def get_notice(db: Session = Depends(get_db)):
    return notice_crud.get_notice_all(db=db)
    

@router.get("/{user_email}", status_code=200)
def get_notice_by_user(user_email: str, db: Session = Depends(get_db)):
    notice =  notice_crud.get_recommand_notice(db=db, user_email=user_email)

    if not notice:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return notice