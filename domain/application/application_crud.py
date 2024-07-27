from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc
from domain.application.application_schema import UserResumeCreate
from models import UserResume


def create_user_resume(db: Session, resume_create: UserResumeCreate):
    version = ""
    try:
        latest_version = int(db.query(UserResume).filter(UserResume.user_email == resume_create.email).order_by(desc(UserResume.version)).first().version)
        version = latest_version + 1
    except:
        version = 1

    print(f"{version} = {resume_create.email}")
    db_resume = UserResume(user_email=resume_create.email,
                           version=version,
                           content=resume_create.content)

    db.add(db_resume)
    db.commit()