from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
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

OCR_API_URL = settings.OCR_API_URL
OCR_SECRET_KEY = settings.OCR_SECRET_KEY
OCR_TEMPLET_IDS = settings.OCR_TEMPLET_IDS

router = APIRouter(
    prefix="/api/user",
)


# 날짜 데이터 형식 변환
def change_str_datetime(date_str):
    patterns = [
        r"(\d{4})\s*\.?\s*(\d{1,2})\s*\.?\s*(\d{1,2})",  # YYYY M. D or YYYY.M.D or YYYY M D
        r"(\d{4})\s*\.?\s*(\d{1,2})\s*\.?\s*(\d{1,2})\."  # YYYY M. D. or YYYY.M.D.
    ]

    for pattern in patterns:
        match = re.match(pattern, date_str)
        if match:
            year, month, day = match.groups()
            # 날짜 문자열을 datetime 객체로 변환
            date_obj = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
            # datetime 객체를 원하는 형식의 문자열로 변환
            return date_obj.strftime("%Y-%m-%d")

# 랜덤 6자리
def generate_random_string(length=6):
    # 문자열에 사용할 문자의 집합 정의
    characters = string.ascii_letters + string.digits
    # 랜덤하게 문자열 생성
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# 텍스트 추출
def get_text_to_image(encoded_string):
    headers = {
        "Content-Type" : "application/json",
        "X-OCR-SECRET": OCR_SECRET_KEY
    }

    request_json = {
        'version': 'V2',
        'requestId': str(uuid.uuid4()),
        'timestamp': int(round(time.time() * 1000)),
        'images': [
            {
                'format': 'jpg',
                'name': 'medium',
                'data': encoded_string,
                'templateIds': OCR_TEMPLET_IDS
            }
        ]
    }

    payload = json.dumps(request_json).encode('UTF-8')
    response = requests.post(OCR_API_URL, headers=headers, data=payload)

    result = response.json()
    # print(result)
    
    # 텍스트 추출
    extracted_text = []
    for field in result['images'][0]['fields']:
        extracted_text.append(field['inferText'])

    return {"template": result['images'][0]['matchedTemplate']['name'], "text": extracted_text}


# 회원가입
@router.post("/craete", status_code=200)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)

# 장애인 등록증 텍스트 추출
@router.post("/upload-image", status_code=200)
async def upload_user_image(file: UploadFile = File(...)):
    # Base64 인코딩을 위해 파일을 읽어들입니다
    file_contents = await file.read()
    
    # 파일 형식 변경
    encoded_string = base64.b64encode(file_contents).decode('utf-8')
    result_text = get_text_to_image(encoded_string)

    # dreamup_복지카드_v2
    card_type = result_text['template']
    text = result_text['text']

    data = {}
    if card_type == "dreamup_복지카드_v2":
        data['name'] = text[0].replace(" ", "")
        data['birth'] = text[1]
        # data['disabled_type']
        data['disabled_level'] = text[2]
        data['address'] = text[3]
        data['issued_date'] = change_str_datetime(text[4])
        data['expiration_period'] = change_str_datetime(text[5])
    else:
        data['name'] = text[0]
        data['birth'] = text[1]
        # data['gender'] = text[2]
        data['disabled_type'] = text[3][:-2]
        data['disabled_level'] = text[3][-2:]
        # data['address']
        data['issued_date'] = change_str_datetime(text[4])
        data['expiration_period'] = change_str_datetime(text[5])
    
    return {"data": data}

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
