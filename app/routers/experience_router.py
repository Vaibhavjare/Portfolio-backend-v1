from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from app.models.experience import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse
)

from app.services.experience_service import ExperienceService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/experiences",
    tags=["Experiences"],
)


# ======================================
# PUBLIC - GET EXPERIENCES
# ======================================

@router.get("/", response_model=List[ExperienceResponse])
async def get_experiences(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    featured: Optional[bool] = None,
):

    return await ExperienceService.get_experiences(
        skip,
        limit,
        search,
        featured
    )


# ======================================
# PUBLIC - GET EXPERIENCE BY UUID
# ======================================

@router.get("/{experience_uuid}", response_model=ExperienceResponse)
async def get_experience(experience_uuid: UUID):

    experience = await ExperienceService.get_experience_by_uuid(
        experience_uuid
    )

    if not experience:
        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    return experience


# ======================================
# ADMIN - CREATE EXPERIENCE
# ======================================

@router.post("/", response_model=ExperienceResponse)
async def create_experience(
    data: ExperienceCreate,
    _=Depends(admin_required),
):

    return await ExperienceService.create_experience(data)


# ======================================
# ADMIN - UPDATE EXPERIENCE
# ======================================

@router.put("/{experience_uuid}", response_model=ExperienceResponse)
async def update_experience(
    experience_uuid: UUID,
    data: ExperienceUpdate,
    _=Depends(admin_required),
):

    experience = await ExperienceService.update_experience(
        experience_uuid,
        data
    )

    if not experience:
        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    return experience


# ======================================
# ADMIN - DELETE EXPERIENCE
# ======================================

@router.delete("/{experience_uuid}")
async def delete_experience(
    experience_uuid: UUID,
    _=Depends(admin_required),
):

    deleted = await ExperienceService.delete_experience(
        experience_uuid
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Experience not found"
        )

    return {"message": "Experience deleted successfully"}