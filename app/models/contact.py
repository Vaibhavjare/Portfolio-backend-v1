from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


# =========================================
# MAIN DOCUMENT
# =========================================

class Contact(Document):
    contact_id: UUID = Field(default_factory=uuid4)

    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: Optional[str] = None
    message: str = Field(..., min_length=5)

    phone: Optional[str] = None
    company: Optional[str] = None

    is_read: bool = False
    replied: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "contacts"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Freelance Opportunity",
                "message": "I would like to discuss a project with you.",
                "phone": "+91 9876543210"
            }
        }


# =========================================
# CREATE SCHEMA (Public Use)
# =========================================

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None


# =========================================
# UPDATE SCHEMA (Admin Use)
# =========================================

class ContactUpdate(BaseModel):
    is_read: Optional[bool] = None
    replied: Optional[bool] = None


# =========================================
# RESPONSE SCHEMA
# =========================================

class ContactResponse(BaseModel):
    id: str
    contact_id: UUID

    name: str
    email: EmailStr
    subject: Optional[str]
    message: str
    phone: Optional[str]
    company: Optional[str]

    is_read: bool
    replied: bool
    created_at: datetime

    class Config:
        from_attributes = True