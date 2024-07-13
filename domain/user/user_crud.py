from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = Users(user_id=user_create.user_id,
                   password=pwd_context.hash(user_create.password1),
                   name=user_create.name,
                   email=user_create.email)
    
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(Users).filter(
        (Users.user_id == user_create.user_id) |
        (Users.email == user_create.email)
    ).first()

def get_user(db: Session, user_id: str):
    return db.query(Users).filter(Users.user_id == user_id).first()
