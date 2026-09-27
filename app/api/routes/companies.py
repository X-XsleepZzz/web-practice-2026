from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.company import CompanyCreate, CompanyRead
from app.services import company_service

router = APIRouter()

@router.get("/companies", response_model=list[CompanyRead])
def read_companies(db: Session = Depends(get_db)):
    return company_service.read_companies(db)

@router.post("/companies", status_code=201, response_model=CompanyRead)
def company_create(company: CompanyCreate, db: Session = Depends(get_db)):
    return company_service.company_create(company, db)

@router.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    return company_service.delete_company(company_id, db)
