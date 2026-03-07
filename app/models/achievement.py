from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


# ==============================
# ACHIEVEMENT DOCUMENT
# ==============================

class Achievement(Document):

    achievement_id: UUID = Field(default_factory=uuid4)

    title: str
    organization: str
    description: Optional[str] = None

    achievement_date: datetime

    position: Optional[str] = None  # Winner, Runner-up, Finalist

    certificate_url: Optional[HttpUrl] = None
    event_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    is_featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "achievements"


# ==============================
# CREATE SCHEMA
# ==============================

class AchievementCreate(BaseModel):

    title: str
    organization: str
    description: Optional[str] = None

    achievement_date: datetime
    position: Optional[str] = None

    certificate_url: Optional[HttpUrl] = None
    event_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = False


# ==============================
# UPDATE SCHEMA
# ==============================

class AchievementUpdate(BaseModel):

    title: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None

    achievement_date: Optional[datetime] = None
    position: Optional[str] = None

    certificate_url: Optional[HttpUrl] = None
    event_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = None


# ==============================
# RESPONSE SCHEMA
# ==============================

class AchievementResponse(BaseModel):

    achievement_id: UUID

    title: str
    organization: str
    description: Optional[str]

    achievement_date: datetime
    position: Optional[str]

    certificate_url: Optional[HttpUrl]
    event_url: Optional[HttpUrl]
    image_url: Optional[HttpUrl]

    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True