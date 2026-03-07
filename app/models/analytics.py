from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


# ==============================
# ANALYTICS DOCUMENT
# ==============================

class Analytics(Document):

    analytics_id: UUID = Field(default_factory=uuid4)

    session_id: str
    page: str

    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None

    referrer: Optional[str] = None

    session_duration: Optional[int] = None  # seconds

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "analytics"


# ==============================
# CREATE SCHEMA
# ==============================

class AnalyticsCreate(BaseModel):

    session_id: str
    page: str

    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    country: Optional[str] = None
    city: Optional[str] = None

    referrer: Optional[str] = None

    session_duration: Optional[int] = None


# ==============================
# RESPONSE
# ==============================

class AnalyticsResponse(BaseModel):

    analytics_id: UUID

    session_id: str
    page: str

    ip_address: Optional[str]
    user_agent: Optional[str]

    country: Optional[str]
    city: Optional[str]

    referrer: Optional[str]

    session_duration: Optional[int]

    created_at: datetime

    class Config:
        from_attributes = True