from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationRead
from app.services import application_service

router = APIRouter()

@router.get(
    "/applications",
    response_model=list[ApplicationRead]
)
def read_applications(
    status: str = "interview",
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return application_service.read_applications(status, limit, db)

@router.post(
    "/applications",
    status_code=201,
    response_model=ApplicationRead
)
def application_create(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    return application_service.application_create(application, db)

@router.patch(
    "/applications/{job_id}",
    response_model=ApplicationRead
)
def application_update(
    job_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    return application_service.application_update(job_id, application_update, db)

@router.delete("/applications/{job_id}")
def delete_application(
    job_id: int,
    db: Session = Depends(get_db)
):
    return application_service.delete_application(job_id, db)

