from beanie import Document
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


# =========================================
# ENUM: Proficiency Level
# =========================================

class ProficiencyLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"
    expert = "Expert"


# =========================================
# MAIN DATABASE MODEL
# =========================================

class Skill(Document):
    # 🔥 Public UUID (used in API)
    skill_id: UUID = Field(default_factory=uuid4)

    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

    rating: int = Field(..., ge=1, le=10)
    proficiency_level: ProficiencyLevel

    category: Optional[str] = None
    years_of_experience: Optional[float] = Field(None, ge=0)

    icon_url: Optional[HttpUrl] = None
    color: Optional[str] = None

    tags: List[str] = Field(default_factory=list)

    featured: bool = False
    display_order: int = 0
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "skills"


# =========================================
# CREATE SCHEMA
# =========================================

class SkillCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    rating: int = Field(..., ge=1, le=10)
    proficiency_level: ProficiencyLevel

    category: Optional[str] = None
    years_of_experience: Optional[float] = Field(None, ge=0)
    icon_url: Optional[HttpUrl] = None
    color: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    featured: bool = False
    display_order: int = 0


# =========================================
# UPDATE SCHEMA
# =========================================

class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    proficiency_level: Optional[ProficiencyLevel] = None

    category: Optional[str] = None
    years_of_experience: Optional[float] = Field(None, ge=0)
    icon_url: Optional[HttpUrl] = None
    color: Optional[str] = None
    tags: Optional[List[str]] = None
    featured: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


# =========================================
# RESPONSE SCHEMA (CLEAN VERSION)
# =========================================

class SkillResponse(BaseModel):
    skill_id: UUID

    name: str
    description: Optional[str] = None
    rating: int
    proficiency_level: ProficiencyLevel

    category: Optional[str] = None
    years_of_experience: Optional[float] = None
    icon_url: Optional[HttpUrl] = None
    color: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    featured: bool
    display_order: int
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )