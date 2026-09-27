from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas.company import CompanyCreate

def read_companies(db: Session):
    return db.scalars(select(Company)).all()

def company_create(company: CompanyCreate, db: Session):
    new_company = Company(**company.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

def delete_company(company_id: int, db: Session):
    target_company = db.get(Company, company_id)
    if target_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(target_company)
    db.commit()
    return Response(status_code=204)
