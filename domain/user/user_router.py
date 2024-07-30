from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from database import SessionLocal, get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from pathlib import Path

import random
import string
import requests
import uuid
import time
import json
import base64
import re

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# UPLOAD_DIR = Path("store")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
)

# 랜덤 6자리
def generate_random_string(length=6):
    # 문자열에 사용할 문자의 집합 정의
    characters = string.ascii_letters + string.digits
    # 랜덤하게 문자열 생성
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# 회원가입
@router.post("/create", status_code=200)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    print(_user_create)
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)
    return "가입 완료"


# 장애인 등록증 텍스트 추출
# @router.post("/upload-image", status_code=200)
# async def upload_user_image(file: UploadFile = File(...)):
#     # Base64 인코딩을 위해 파일을 읽어들입니다
#     file_contents = await file.read()
    
#     # 파일 형식 변경
#     encoded_string = base64.b64encode(file_contents).decode('utf-8')
#     result_text = user_crud.get_text_to_image(encoded_string)

#     return {"data": result_text}


@router.post("/upload-image", status_code=200)
async def upload_user_image(): #file: user_schema.UploadImage
    # Base64 인코딩된 파일을 받아
    # 파일 형식 변경
    # result_text = user_crud.get_text_to_image(file.file)

    # return {"data": result_text}
    return 	{

                "name": "홍길동",
                "birth": "123456-1",
                "disabled_level": "4급",
                "address": "서울특별시 종로구",
                "issued_date": "2015-12-31",
                "expiration_period": "2011-06-14"

            }


# 로그인
@router.post("/login", response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("2---------------------")
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        print("2---------------------")
        user = user_crud.get_user(db, email=username)
        print("3---------------------")
        if user is None:
            raise credentials_exception
        return user