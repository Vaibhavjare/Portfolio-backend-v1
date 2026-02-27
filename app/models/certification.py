from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


# =========================================
# MAIN DOCUMENT (Mongo Collection)
# =========================================

class Certificate(Document):
    certificate_id: UUID = Field(default_factory=uuid4)

    name: str = Field(..., min_length=3)
    description: Optional[str] = None

    organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

    certificate_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None

    is_featured: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "certificates"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gen AI Foundational Models for NLP",
                "description": "Certification on Generative AI and NLP models.",
                "organization": "IBM",
                "credential_url": "https://example.com/certificate",
                "certificate_url": "https://example.com/download",
                "is_featured": True
            }
        }


# =========================================
# CREATE SCHEMA
# =========================================

class CertificateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None
    certificate_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    is_featured: Optional[bool] = False


# =========================================
# UPDATE SCHEMA
# =========================================

class CertificateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    organization: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None
    certificate_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    is_featured: Optional[bool] = None


# =========================================
# RESPONSE SCHEMA
# =========================================

class CertificateResponse(BaseModel):
    id: str
    certificate_id: UUID

    name: str
    description: Optional[str]
    organization: Optional[str]

    issue_date: Optional[datetime]
    expiry_date: Optional[datetime]

    credential_id: Optional[str]
    credential_url: Optional[HttpUrl]
    certificate_url: Optional[HttpUrl]
    thumbnail_url: Optional[HttpUrl]

    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True