from datetime import timedelta, datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

from config import settings

import random
import string
import requests
import uuid
import time
import json
import base64
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

OCR_API_URL = settings.OCR_API_URL
OCR_SECRET_KEY = settings.OCR_SECRET_KEY
# OCR_TEMPLET_IDS = settings.OCR_TEMPLET_IDS
OCR_TEMPLET_IDS = [31277, 31278]

def create_user(db: Session, user_create: UserCreate):
    db_user = User(
                    # name=user_create.name,
                #    birth=user_create.birth,
                #    disabled_type=user_create.disabled_type,
                #    disabled_level=user_create.disabled_level,
                #    address=user_create.address,
                #    issued_date=user_create.issued_date,
                #    expiration_period=user_create.expiration_period,
                    email=user_create.email,
                   password=pwd_context.hash(user_create.password),
                   )
    
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        User.email == user_create.email
    ).first()

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


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

    # print(response.status_code)
    # print(f"Response Text: {response.text}")
    
    result = response.json()
    
    # 텍스트 추출
    extracted_text = []
    for field in result['images'][0]['fields']:
        extracted_text.append(field['inferText'])

    # dreamup_복지카드_v2
    card_type = result['images'][0]['matchedTemplate']['name']
    text = extracted_text

    data = {}
    if card_type == "dreamup_복지카드_v2":
        data['name'] = text[0].replace(" ", "")
        data['birth'] = text[1][:-6]
        # data['disabled_type']
        data['disabled_level'] = text[2]
        data['address'] = text[3]
        data['issued_date'] = change_str_datetime(text[4])
        data['expiration_period'] = change_str_datetime(text[5])
    else:
        data['name'] = text[0]
        data['birth'] = text[1].replace(".","")
        if int(data['birth']) > 300000:
            if text[2] == "남":
                data['birth'] += "-1"
            else:
                data['birth'] += "-2"
        else:
            if text[2] == "남":
                data['birth'] += "-3"
            else:
                data['birth'] += "-4"
        data['disabled_type'] = text[3][:-2]
        data['disabled_level'] = text[3][-2:]
        # data['address']
        data['issued_date'] = change_str_datetime(text[4])
        data['expiration_period'] = change_str_datetime(text[5])

    return data
