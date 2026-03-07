from beanie import Document
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List


# ==============================
# BLOG DOCUMENT
# ==============================

class Blog(Document):

    blog_id: UUID = Field(default_factory=uuid4)

    title: str
    slug: str

    summary: Optional[str] = None
    content: str

    tags: List[str] = Field(default_factory=list)

    cover_image: Optional[HttpUrl] = None

    is_published: bool = False
    is_featured: bool = False

    published_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blogs"


# ==============================
# CREATE SCHEMA
# ==============================

class BlogCreate(BaseModel):

    title: str
    slug: str

    summary: Optional[str] = None
    content: str

    tags: Optional[List[str]] = []

    cover_image: Optional[HttpUrl] = None

    is_published: Optional[bool] = False
    is_featured: Optional[bool] = False


# ==============================
# UPDATE SCHEMA
# ==============================

class BlogUpdate(BaseModel):

    title: Optional[str] = None
    slug: Optional[str] = None

    summary: Optional[str] = None
    content: Optional[str] = None

    tags: Optional[List[str]] = None

    cover_image: Optional[HttpUrl] = None

    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None


# ==============================
# RESPONSE SCHEMA
# ==============================

class BlogResponse(BaseModel):

    blog_id: UUID

    title: str
    slug: str

    summary: Optional[str]
    content: str

    tags: List[str]

    cover_image: Optional[HttpUrl]

    is_published: bool
    is_featured: bool

    published_at: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True