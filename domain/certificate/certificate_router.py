from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from config import settings
from database import SessionLocal, get_db
from domain.certificate import certificate_crud, certificate_schema

router = APIRouter(
    prefix="/api/certification",
)

@router.get("", status_code=200)
def resume_create(db: Session = Depends(get_db)):
    data = certificate_crud.get_certification(db=db)
    print(type(data))

    return data