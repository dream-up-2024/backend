from datetime import timedelta, datetime

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
# from domain.notice.notice_schema import UserCreate
from models import Notice, User, UserResume

from config import settings

import pandas as pd

# 미추천 모든 공고 리스트 반환
def get_notice_all(db: Session):
    notices = db.query(Notice).order_by(Notice.deadline).all()
    return notices

# 추천 공고 리스트 반환
def get_recommand_notice(db: Session, user_email):
    # try:
        user = db.query(User).filter(User.email == user_email).one()

        recommand_job_1 = user.recommand_job_1
        recommand_job_2 = user.recommand_job_2
        recommand_job_3 = user.recommand_job_3

        # 지역 기반 공고 반환
        if recommand_job_1 == '' and recommand_job_2 == '' and recommand_job_3 == '':
            # print(f"{user.address[:2]} / {user.address.split(" ")[1][:2]}")
            return db.query(Notice).filter(Notice.address1 == user.address[:2]).order_by(Notice.deadline).all()

        # 추천 직무-이력서의 거주지 기반 공고 반환
        resume = db.query(UserResume).filter(UserResume.user_email == user_email).order_by(desc(UserResume.version)).first().content
        return db.query(Notice).filter(or_(Notice.job_type.in_((recommand_job_1, recommand_job_2, recommand_job_3)), Notice.address1 == resume['residence'][:2])).order_by(Notice.deadline).all()
    # except:
    #     return False


def create_notice_list(db: Session):
    # notices = pd.read_csv(f'/Users/ryeon/Documents/Project/dacon/data_store/notice_20240731_2058_v3.csv', encoding='utf-8-sig').fillna("")
    notices = pd.read_csv(f'/Users/ryeon/Documents/Project/dacon/data_store/work_data/final_20240729.csv', encoding='utf-8-sig')
    for index, row in notices.iterrows():
        data = row.to_dict()
        db_notice = Notice(
            company=data['office'],
            title=data['title'],
            job_type=data['main_category'],
            url="https://www.work.go.kr" + data['url'],
            work_experience=data['career'],
            education=data['education'],
            address1=data['address'].split(" ")[0][:2],
            address2=data['address'].split(" ")[1],
            working_hour=data['working_day'],
            deadline=data['deadline'],
        )
        db.add(db_notice)

    db.commit()
