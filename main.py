import os
from pathlib import Path
from datetime import date, datetime
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, Date, DateTime, Enum, Integer, ForeignKey, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session

app = FastAPI()

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db

class Base(DeclarativeBase):
    pass

class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable = False)
    company: Mapped["Company"] = relationship(
        back_populates="applications"
    )
    role: Mapped[str] = mapped_column(
        String(30),
        nullable = False
        )
    status: Mapped[str] = mapped_column(
        Enum(
            "interested",
            "applied",
            "interview",
            "offer",
            "rejected",
            "withdrawn",
            name = "application_status"
        ),
        nullable = False,
        index = True
    )
    job_url: Mapped[str | None] = mapped_column(
        String,
        nullable = True
    )
    deadline: Mapped[date | None] = mapped_column(
        Date,
        nullable = True
    )
    notes: Mapped[str | None] = mapped_column(
        String(150),
        nullable = True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable = False,
        default = datetime.now
    )
    applied_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable = True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable = False,
        default = datetime.now,
        onupdate = datetime.now
    )
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    applications: Mapped[list["Application"]] = relationship(
        back_populates="company",
        cascade="all, delete",
        passive_deletes=True,
    )

class ApplicationCreate(BaseModel):
    company_id: int
    role: str
    status: Literal[
        "interested",
        "applied",
        "interview",
        "offer",
        "rejected",
        "withdrawn",
    ]
    job_url: str | None = None
    applied_at: datetime | None = None
    deadline: date
    notes: str | None = None

class ApplicationUpdate(BaseModel):
    company_id: int | None = None
    role: str | None = None
    status: Literal[
        "interested",
        "applied",
        "interview",
        "offer",
        "rejected",
        "withdrawn",
        ] | None = None
    job_url: str | None = None
    applied_at: datetime | None = None
    deadline: date | None = None
    notes: str | None = None

class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    company_id: int
    role: str
    status: Literal[
        "interested",
        "applied",
        "interview",
        "offer",
        "rejected",
        "withdrawn",
    ]
    job_url: str | None = None
    applied_at: datetime | None = None
    deadline: date | None
    notes: str | None = None
    created_at: datetime

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    website: str | None = None

class CompanyRead(CompanyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

@app.get("/")
def root():
    return {"message": "job tracker api"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get(
    "/applications",
    response_model=list[ApplicationRead]
)
def read_applications(
    status: str = "interview",
    limit: int = 10,
    db: Session = Depends(get_db)
):
    valid_status = [
        "interested",
        "applied",
        "interview",
        "offer",
        "rejected",
        "withdrawn",
    ]

    if limit < 1 or 100 < limit:
        raise HTTPException(
            status_code=400,
            detail="Invalid limit"
        )

    if status not in valid_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    stmt = (
        select(Application)
        .where(Application.status == status)
        .limit(limit)
    )

    results = db.scalars(stmt).all()

    return results

@app.post(
    "/applications",
    status_code=201,
    response_model=ApplicationRead
)
def application_create(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    if db.get(Company, application.company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")

    new_application = Application(
        **application.model_dump()
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@app.patch(
    "/applications/{job_id}",
    response_model=ApplicationRead
)
def application_update(
    job_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    stmt = select(Application).where(
        Application.id == job_id
    )

    target_application = db.scalars(stmt).first()

    if target_application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    update_data = application_update.model_dump(
        exclude_unset=True
    )

    if "company_id" in update_data:
        if update_data["company_id"] is None:
            raise HTTPException(status_code=422, detail="company_id cannot be null")
        if db.get(Company, update_data["company_id"]) is None:
            raise HTTPException(status_code=404, detail="Company not found")

    for field, value in update_data.items():
        setattr(target_application, field, value)

    db.commit()
    db.refresh(target_application)

    return target_application


    if job_id not in applications:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    del applications[job_id]
    return Response(status_code=204)

@app.delete("/applications/{job_id}")
def delete_application(
    job_id: int,
    db: Session = Depends(get_db)
):
    stmt = select(Application).where(
        Application.id == job_id
    )

    target_application = db.scalars(stmt).first()

    if target_application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(target_application)
    db.commit()

    return Response(status_code=204)

@app.get("/companies", response_model=list[CompanyRead])
def read_companies(db: Session = Depends(get_db)):
    return db.scalars(select(Company)).all()

@app.post("/companies", status_code=201, response_model=CompanyRead)
def company_create(company: CompanyCreate, db: Session = Depends(get_db)):
    new_company = Company(**company.model_dump())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@app.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    target_company = db.get(Company, company_id)
    if target_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(target_company)
    db.commit()
    return Response(status_code=204)

