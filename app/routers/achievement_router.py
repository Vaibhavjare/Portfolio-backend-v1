from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from app.models.achievement import (
    AchievementCreate,
    AchievementUpdate,
    AchievementResponse
)

from app.services.achievement_service import AchievementService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/achievements",
    tags=["Achievements"],
)


# ==============================
# PUBLIC GET
# ==============================

@router.get("/", response_model=List[AchievementResponse])
async def get_achievements(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    featured: Optional[bool] = None
):

    return await AchievementService.get_achievements(
        skip,
        limit,
        featured
    )


# ==============================
# GET SINGLE
# ==============================

@router.get("/{achievement_uuid}", response_model=AchievementResponse)
async def get_achievement(achievement_uuid: UUID):

    achievement = await AchievementService.get_achievement_by_uuid(
        achievement_uuid
    )

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    return achievement


# ==============================
# ADMIN CREATE
# ==============================

@router.post("/", response_model=AchievementResponse)
async def create_achievement(
    data: AchievementCreate,
    _=Depends(admin_required)
):

    return await AchievementService.create_achievement(data)


# ==============================
# ADMIN UPDATE
# ==============================

@router.put("/{achievement_uuid}", response_model=AchievementResponse)
async def update_achievement(
    achievement_uuid: UUID,
    data: AchievementUpdate,
    _=Depends(admin_required)
):

    achievement = await AchievementService.update_achievement(
        achievement_uuid,
        data
    )

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    return achievement


# ==============================
# ADMIN DELETE
# ==============================

@router.delete("/{achievement_uuid}")
async def delete_achievement(
    achievement_uuid: UUID,
    _=Depends(admin_required)
):

    deleted = await AchievementService.delete_achievement(
        achievement_uuid
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    return {"message": "Achievement deleted successfully"}