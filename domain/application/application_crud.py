from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from domain.application.application_schema import UserResumeCreate, UserCoverLetterCreate
from models import UserResume, UserCoverLetter, User

# 이력서 생성
def create_user_resume(db: Session, resume_create: UserResumeCreate, user_email):
    version = ""
    try:
        latest_version = int(
            db.query(UserResume)
            .filter(UserResume.user_email == resume_create.email)
            .order_by(desc(UserResume.version))
            .first().version)
        version = latest_version + 1
    except:
        version = 1

    print(f"{version} = {resume_create}")
    db_resume = UserResume(user_email=user_email,
                           version=version,
                           content=resume_create.content)

    # 유저별 추천 직무 변경 - return 필요

    db.add(db_resume)
    db.commit()

# 자기소개서 추가
def create_user_cover_letter(db: Session, cover_letter_create: UserCoverLetterCreate, user_email, type):
    # # 자기소개서 작성 요청
    # 입력된 데이터
    input_data = cover_letter_create.content
    
    # 추가 데이터 가져오기
    # user = db.query(User).filter(User.email == user_email)
    # resume = db.query(UserResume).filter(UserResume.user_email == user_email).order_by(desc(UserResume.version)).first()

    # question = {
    #     "user_informaiton": {
    #         "birth": user.birth,
    #         "disabled_type": user.disabled_type,
    #         "disabled_level": user.disabled_level,
    #         "address": user.address
    #     },
    #     "user_resume": {

    #     }
    # }
    
    # 작성된 자기소개서 저장 및 반환
    version = ""
    try:
        latest_version = int(db.query(UserCoverLetter).filter(
            and_(UserCoverLetter.user_email == cover_letter_create.user_email,
                 UserCoverLetter.type == cover_letter_create.type)
        ).order_by(desc(UserCoverLetter.version)).first().version)
        version = latest_version + 1
    except:
        version = 1

    print(f"{version} = {user_email}")

    db_cover_letter = UserCoverLetter(user_email=user_email,
                            type = type,
                           version=version,
                           content=cover_letter_create.content)

    db.add(db_cover_letter)
    db.commit()

# 유저 별 이력서 내용 반환
def get_user_resume(db: Session, user_email):
    resume = db.query(UserResume).filter(UserResume.user_email == user_email).order_by(desc(UserResume.version)).first()
    return resume

def get_user_cover_letter(db: Session, user_email):
    # 1: 지원동기: Motivation for Application / 2: 성장배경: Background and Growth / 3: 성격의 장단점: Strengths and Weaknesses of Personality
    motivation = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "1")).order_by(desc(UserCoverLetter.version)).first()
    growth = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "2")).order_by(desc(UserCoverLetter.version)).first()
    personality = db.query(UserCoverLetter).filter(and_(UserCoverLetter.user_email == user_email, UserCoverLetter.type == "3")).order_by(desc(UserCoverLetter.version)).first()

    return [motivation, growth, personality]
