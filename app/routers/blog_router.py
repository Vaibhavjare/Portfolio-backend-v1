from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from app.models.blog import (
    BlogCreate,
    BlogUpdate,
    BlogResponse
)

from app.services.blog_service import BlogService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"],
)


# ==============================
# PUBLIC GET BLOGS
# ==============================

@router.get("/", response_model=List[BlogResponse])
async def get_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    featured: Optional[bool] = None
):

    return await BlogService.get_blogs(
        skip,
        limit,
        featured
    )


# ==============================
# GET SINGLE BLOG
# ==============================

@router.get("/{blog_uuid}", response_model=BlogResponse)
async def get_blog(blog_uuid: UUID):

    blog = await BlogService.get_blog_by_uuid(
        blog_uuid
    )

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return blog


# ==============================
# ADMIN CREATE
# ==============================

@router.post("/", response_model=BlogResponse)
async def create_blog(
    data: BlogCreate,
    _=Depends(admin_required)
):

    return await BlogService.create_blog(data)


# ==============================
# ADMIN UPDATE
# ==============================

@router.put("/{blog_uuid}", response_model=BlogResponse)
async def update_blog(
    blog_uuid: UUID,
    data: BlogUpdate,
    _=Depends(admin_required)
):

    blog = await BlogService.update_blog(
        blog_uuid,
        data
    )

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return blog


# ==============================
# ADMIN DELETE
# ==============================

@router.delete("/{blog_uuid}")
async def delete_blog(
    blog_uuid: UUID,
    _=Depends(admin_required)
):

    deleted = await BlogService.delete_blog(
        blog_uuid
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    return {"message": "Blog deleted successfully"}