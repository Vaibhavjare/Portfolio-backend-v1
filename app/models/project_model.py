# app/models/project_model.py

from beanie import Document
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime


# =========================================
# Embedded Model: Tech Stack
# =========================================

class TechStack(BaseModel):
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


# =========================================
# DATABASE DOCUMENT (Mongo Internal)
# =========================================

class Project(Document):
    # 🔥 Public ID (used in API)
    project_id: UUID = Field(default_factory=uuid4)

    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10)

    tech_stack: TechStack

    github_link: Optional[HttpUrl] = None
    video_links: List[HttpUrl] = Field(default_factory=list)
    thumbnail_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

    complexity_score: int = Field(..., ge=1, le=10)
    featured: bool = False
    tags: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "projects"


# =========================================
# CREATE SCHEMA
# =========================================

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10)
    tech_stack: TechStack

    github_link: Optional[HttpUrl] = None
    video_links: List[HttpUrl] = Field(default_factory=list)
    thumbnail_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

    complexity_score: int = Field(..., ge=1, le=10)
    featured: bool = False
    tags: List[str] = Field(default_factory=list)


# =========================================
# UPDATE SCHEMA
# =========================================

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, min_length=10)
    tech_stack: Optional[TechStack] = None

    github_link: Optional[HttpUrl] = None
    video_links: Optional[List[HttpUrl]] = None
    thumbnail_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

    complexity_score: Optional[int] = Field(None, ge=1, le=10)
    featured: Optional[bool] = None
    tags: Optional[List[str]] = None


# =========================================
# RESPONSE MODEL (NO _id, NO ObjectId)
# =========================================

class ProjectResponse(BaseModel):
    project_id: UUID

    title: str
    description: str
    tech_stack: TechStack

    github_link: Optional[HttpUrl] = None
    video_links: List[HttpUrl] = Field(default_factory=list)
    thumbnail_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

    complexity_score: int
    featured: bool
    tags: List[str] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )