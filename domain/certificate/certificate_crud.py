from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from domain.certificate import *
from models import Certificate


def get_certification(db: Session):
    certificate_rows = db.query(Certificate.name).all()
    certificates = [row[0] for row in certificate_rows]
    return certificates