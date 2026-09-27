from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import date, datetime

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
