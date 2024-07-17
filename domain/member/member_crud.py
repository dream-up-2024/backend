from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.member.member_schema import MemberCreate
from models import Members

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_member(db: Session, member_create: MemberCreate):
    member = Members(name = member_create.name,
                birth = member_create.birth,
                disabled_type = member_create.disabled_type,
                disabled_level = member_create.disabled_level,
                address = member_create.address,
                issued_date = member_create.issued_date,
                expiration_period = member_create.expiration_period,
                email = member_create.email,
                password = pwd_context.hash(member_create.password1),)
    
    db.add(member)
    db.commit()

def get_existing_member(db: Session, member_create: MemberCreate):
    return db.query(Members).filter(
        (Members.email == member_create.email)
    ).first()

def get_member(db: Session, member_email: str):
    return db.query(Members).filter(Members.email == member_email).first()