from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


# ==============================
# EDUCATION DOCUMENT
# ==============================

class Education(Document):

    education_id: UUID = Field(default_factory=uuid4)

    institution: str
    degree: str
    field_of_study: str

    start_date: datetime
    end_date: Optional[datetime] = None

    grade: Optional[str] = None
    description: Optional[str] = None

    institution_logo: Optional[HttpUrl] = None
    institution_url: Optional[HttpUrl] = None

    is_featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "educations"


# ==============================
# CREATE SCHEMA
# ==============================

class EducationCreate(BaseModel):

    institution: str
    degree: str
    field_of_study: str

    start_date: datetime
    end_date: Optional[datetime] = None

    grade: Optional[str] = None
    description: Optional[str] = None

    institution_logo: Optional[HttpUrl] = None
    institution_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = False


# ==============================
# UPDATE SCHEMA
# ==============================

class EducationUpdate(BaseModel):

    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    grade: Optional[str] = None
    description: Optional[str] = None

    institution_logo: Optional[HttpUrl] = None
    institution_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = None


# ==============================
# RESPONSE SCHEMA
# ==============================

class EducationResponse(BaseModel):

    education_id: UUID

    institution: str
    degree: str
    field_of_study: str

    start_date: datetime
    end_date: Optional[datetime]

    grade: Optional[str]
    description: Optional[str]

    institution_logo: Optional[HttpUrl]
    institution_url: Optional[HttpUrl]

    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True