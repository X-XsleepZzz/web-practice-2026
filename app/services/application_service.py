from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Application, Company
from app.schemas.application import ApplicationCreate, ApplicationUpdate

def read_applications(
    status: str = "interview",
    limit: int = 10,
    db: Session = None
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

def application_create(
    application: ApplicationCreate,
    db: Session = None
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

def application_update(
    job_id: int,
    application_update: ApplicationUpdate,
    db: Session = None
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

def delete_application(
    job_id: int,
    db: Session = None
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

