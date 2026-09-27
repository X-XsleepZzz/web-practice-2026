from pydantic import BaseModel, ConfigDict, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    website: str | None = None

class CompanyRead(CompanyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
