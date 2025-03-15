from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.company import Company
from app.schemas.company import CompanyCreate


def create_company(db: Session, company: CompanyCreate):
    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return status.HTTP_201_CREATED


def get_all_companies(db: Session):
    return db.query(Company).all()


def get_company_by_id(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()


def update_company(db: Session, company: CompanyCreate, company_id: int):
    db_company = get_company_by_id(db, company_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Companyia no trobada")

    for key, value in company.model_dump().items():
        setattr(db_company, key, value)
        db.commit()
        db.refresh(db_company)
    return status.HTTP_200_OK