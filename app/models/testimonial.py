from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


# ==============================
# TESTIMONIAL DOCUMENT
# ==============================

class Testimonial(Document):

    testimonial_id: UUID = Field(default_factory=uuid4)

    name: str
    role: Optional[str] = None
    company: Optional[str] = None

    message: str

    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    is_featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "testimonials"


# ==============================
# CREATE SCHEMA
# ==============================

class TestimonialCreate(BaseModel):

    name: str
    role: Optional[str] = None
    company: Optional[str] = None

    message: str

    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = False


# ==============================
# UPDATE SCHEMA
# ==============================

class TestimonialUpdate(BaseModel):

    name: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None

    message: Optional[str] = None

    avatar_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    is_featured: Optional[bool] = None


# ==============================
# RESPONSE SCHEMA
# ==============================

class TestimonialResponse(BaseModel):

    testimonial_id: UUID

    name: str
    role: Optional[str]
    company: Optional[str]

    message: str

    avatar_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]

    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True