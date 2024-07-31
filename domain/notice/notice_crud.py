from datetime import timedelta, datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
# from domain.notice.notice_schema import UserCreate
from models import Notice, User

from config import settings

import pandas as pd


def get_notice_all(db: Session):
    notices = db.query(Notice).order_by(Notice.deadline).all()
    return notices


# def create_notice_list(db: Session):
#     notices = pd.read_csv(f'/Users/ryeon/Documents/Project/dacon/data_store/notice_20240731_2058_v3.csv', encoding='utf-8-sig').fillna("")
    
#     for index, row in notices.iterrows():
#         data = row.to_dict()
#         db_notice = Notice(
#             company=data['company'],
#             title=data['title'],
#             job_type=data['job_type'],
#             url=data['url'],
#             work_experience=data['work_experience'],
#             education=data['education'],
#             address1=data['region'],
#             address2=data['txt'],
#             working_hour=data['working_hour'],
#             deadline=data['deadline'],
#         )
#         db.add(db_notice)

#     db.commit()
