from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
from bson import ObjectId


# ==============================
# EXPERIENCE DOCUMENT
# ==============================

class Experience(Document):

    experience_id: UUID = Field(default_factory=uuid4)

    company: str
    role: str
    description: str

    location: Optional[str] = None

    technologies: Optional[List[str]] = []

    start_date: datetime
    end_date: Optional[datetime] = None

    company_logo: Optional[HttpUrl] = None
    company_url: Optional[HttpUrl] = None

    is_current: bool = False
    is_featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "experiences"


# ==============================
# CREATE SCHEMA
# ==============================

class ExperienceCreate(BaseModel):

    company: str
    role: str
    description: str

    location: Optional[str] = None
    technologies: Optional[List[str]] = []

    start_date: datetime
    end_date: Optional[datetime] = None

    company_logo: Optional[HttpUrl] = None
    company_url: Optional[HttpUrl] = None

    is_current: Optional[bool] = False
    is_featured: Optional[bool] = False


# ==============================
# UPDATE SCHEMA
# ==============================

class ExperienceUpdate(BaseModel):

    company: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None

    location: Optional[str] = None
    technologies: Optional[List[str]] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    company_logo: Optional[HttpUrl] = None
    company_url: Optional[HttpUrl] = None

    is_current: Optional[bool] = None
    is_featured: Optional[bool] = None


# ==============================
# RESPONSE SCHEMA
# ==============================

class ExperienceResponse(BaseModel):

    experience_id: UUID

    company: str
    role: str
    description: str

    location: Optional[str]
    technologies: Optional[List[str]]

    start_date: datetime
    end_date: Optional[datetime]

    company_logo: Optional[HttpUrl]
    company_url: Optional[HttpUrl]

    is_current: bool
    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True