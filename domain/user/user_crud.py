from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(name=user_create.name,
                   birth=user_create.birth,
                   disabled_type=user_create.disabled_type,
                   disabled_level=user_create.disabled_level,
                   address=user_create.address,
                   issued_date=user_create.issued_date,
                   expiration_period=user_create.expiration_period,
                   email=user_create.email,
                   password=pwd_context.hash(user_create.password1),
                   )
    
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        User.email == user_create.email
    ).first()

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
