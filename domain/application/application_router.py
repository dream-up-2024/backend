from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from database import SessionLocal, get_db
from domain.application import application_crud, application_schema

router = APIRouter(
    prefix="/api/application",
)

# 이력서 작성
@router.post("/resume", status_code=200)
def resume_create(_resume_create: application_schema.UserResumeCreate, db: Session = Depends(get_db)):
    application_crud.create_user_resume(db=db, resume_create=_resume_create)