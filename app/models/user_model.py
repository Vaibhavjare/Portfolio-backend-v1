# user_model.py

from beanie import Document
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional


# =========================================
# ROLE ENUM
# =========================================

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


# =========================================
# SOCIAL LINKS OBJECT
# =========================================

class SocialLinks(BaseModel):
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None
    instagram: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None


# =========================================
# MAIN USER DOCUMENT
# =========================================

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)

    # ======================
    # Auth Fields
    # ======================
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = True

    # ======================
    # Portfolio Profile Fields
    # ======================
    full_name: Optional[str] = None
    title: Optional[str] = None
    objective: Optional[str] = None
    bio: Optional[str] = None

    experience_years: Optional[int] = None
    skills_summary: Optional[str] = None

    phone: Optional[str] = None
    location: Optional[str] = None

    profile_photo: Optional[HttpUrl] = None
    cover_image: Optional[HttpUrl] = None
    resume_url: Optional[HttpUrl] = None

    social_links: Optional[SocialLinks] = None

    is_public: bool = True  # 🔥 Important for public profile visibility

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"


# =========================================
# PROFILE UPDATE SCHEMA (ADMIN ONLY)
# =========================================

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    title: Optional[str] = None
    objective: Optional[str] = None
    bio: Optional[str] = None

    experience_years: Optional[int] = None
    skills_summary: Optional[str] = None

    phone: Optional[str] = None
    location: Optional[str] = None

    profile_photo: Optional[HttpUrl] = None
    cover_image: Optional[HttpUrl] = None
    resume_url: Optional[HttpUrl] = None

    social_links: Optional[SocialLinks] = None
    is_public: Optional[bool] = None


# =========================================
# PUBLIC PROFILE RESPONSE
# =========================================

class UserProfileResponse(BaseModel):
    user_id: UUID

    full_name: Optional[str]
    title: Optional[str]
    objective: Optional[str]
    bio: Optional[str]

    experience_years: Optional[int]
    skills_summary: Optional[str]

    email: EmailStr
    phone: Optional[str]
    location: Optional[str]

    profile_photo: Optional[HttpUrl]
    cover_image: Optional[HttpUrl]
    resume_url: Optional[HttpUrl]

    social_links: Optional[SocialLinks]

    class Config:
        from_attributes = True