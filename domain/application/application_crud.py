from passlib.context import CryptContext
from sqlalchemy.orm import Session, class_mapper
from sqlalchemy import desc, and_
from domain.application.application_schema import UserResumeCreate, UserCoverLetterCreate
from domain.gptapi import recommand
from models import UserResume, UserCoverLetter, User

import json

# 직무 추천을 위한 적용
def check_data_by_user(db, user):
    user_info = {}
    
    try:
        user_info["user"] = {
            "birth": user.birth,
            "disabled_type": user.disabled_type,
            "disabled_level": user.disabled_level
        }
    except:
        return False

    try:
        user_resume = db.query(UserResume).filter(UserResume.user_email == user.email).order_by(desc(UserResume.version)).first()
        # user_resume = {c.key: getattr(user_resume, c.key) for c in class_mapper(user_resume.__class__).columns}
        # user_resume.pop('id')
        user_info["user_resume"] = user_resume.content
    except:
        user_info["user_resume"] = ""
    try:
        cover_letter_types = ["지원동기", "성장배경", "성격의장단점"]
        for type in cover_letter_types:
            user_cover_letter = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user.email)==type).order_by(desc(UserCoverLetter.version)).first()    
            # user_cover_letter = {c.key: getattr(user_cover_letter, c.key) for c in class_mapper(user_cover_letter.__class__).columns}
            # user_cover_letter.pop('id')
            user_info["user_cover_letter"][type] = user_cover_letter.content
    except:
        user_info["user_cover_letter"] = ""

    return user_info

# 이력서 생성
def create_user_resume(db: Session, resume_create: UserResumeCreate, user_email):
    version = ""
    try:
        latest_version = int(
            db.query(UserResume)
            .filter(UserResume.user_email == user_email)
            .order_by(desc(UserResume.version))
            .first().version)
        version = latest_version + 1
    except:
        version = 1

    db_resume = UserResume(user_email=user_email,
                           version=version,
                           content=resume_create.content)

    db.add(db_resume)

    # 추천 직무 변경
    db_user = db.query(User).filter(User.email == user_email).one()
    recommand_based_data = check_data_by_user(db, db_user)

    recommand_job= recommand.start_recommand_job(recommand_based_data)

    db_user.recommand_job_1 = recommand_job[0]
    db_user.recommand_job_2 = recommand_job[1]
    db_user.recommand_job_3 = recommand_job[2]

    db.commit()


# 자기소개서 생성
def create_user_cover_letter(db: Session, cover_letter_create: UserCoverLetterCreate, user_email):
    ## 자기소개서 작성 요청
    # 입력된 데이터
    type = cover_letter_create.type
    input_data = cover_letter_create.content

    db_user = db.query(User).filter(User.email == user_email).one()
    recommand_based_data = check_data_by_user(db, db_user)
    recommand_based_data.pop('user_cover_letter')
    # user_info = {
    #         "birth": user.birth,
    #         "disabled_type": user.disabled_type,
    #         "disabled_level": user.disabled_level,
    #     }
    gpt_question = input_data
    
    final_cover_letter = recommand.recommand_cover_letter(type, recommand_based_data, gpt_question)

    # print(f"{version} = {user_email}")
    version = ""
    try:
        latest_version = int(
            db.query(UserCoverLetter)
            .filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == type))
            .order_by(desc(UserCoverLetter.version))
            .first().version)
        version = latest_version + 1
    except:
        version = 1

    db_cover_letter = UserCoverLetter(user_email=user_email,
                            type = type,
                            version=version,
                            content=final_cover_letter)

    db.add(db_cover_letter)

    # 추천 직무 변경
    db_user = db.query(User).filter(User.email == user_email).one()
    recommand_based_data = check_data_by_user(db, db_user)

    recommand_job = recommand.start_recommand_job(recommand_based_data)

    db_user.recommand_job_1 = recommand_job[0]
    db_user.recommand_job_2 = recommand_job[1]
    db_user.recommand_job_3 = recommand_job[2]
    db.commit()
    
    return final_cover_letter


# 유저 별 이력서 내용 반환
def get_user_resume(db: Session, user_email):
    resume = db.query(UserResume).filter(UserResume.user_email == user_email).order_by(desc(UserResume.version)).first()
    return resume

# 유저 별 자기소개서 내용 반환
def get_user_cover_letter(db: Session, user_email):
    # 1: 지원동기: Motivation for Application
    # 2: 성장배경: Background and Growth
    # 3: 성격의 장단점: Strengths and Weaknesses of Personality
    motivation = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "지원동기")).order_by(desc(UserCoverLetter.version)).first()
    growth = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "성장배경")).order_by(desc(UserCoverLetter.version)).first()
    personality = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "성격의장단점")).order_by(desc(UserCoverLetter.version)).first()

    # return [motivation, growth, personality]
    return [len(motivation), len(growth), len(personality)]

# 유저 별 자기소개서 내용 반환 - 타입별
def get_user_cover_letter_by_type(db: Session, user_email, type):
    # 1: 지원동기: Motivation for Application
    # 2: 성장배경: Background and Growth
    # 3: 성격의 장단점: Strengths and Weaknesses of Personality
    if type == 1:
        data = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "지원동기")).order_by(desc(UserCoverLetter.version)).first()
    elif type == 2:
        data = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "성장배경")).order_by(desc(UserCoverLetter.version)).first()
    elif data == 3:
        data = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "성격의장단점")).order_by(desc(UserCoverLetter.version)).first()

    return data
