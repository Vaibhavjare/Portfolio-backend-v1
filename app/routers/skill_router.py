# app/routers/skill_router.py

from fastapi import APIRouter, Query, Depends, status
from typing import List, Optional
from uuid import UUID

from app.models.skill import (
    SkillCreate,
    SkillUpdate,
    SkillResponse,
)
from app.services.skill_service import SkillService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)


# =========================================
# PUBLIC ROUTES
# =========================================

@router.get(
    "/",
    response_model=List[SkillResponse],
    status_code=status.HTTP_200_OK,
)
async def get_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("display_order"),
    order: str = Query("asc"),
):
    return await SkillService.get_skills(
        skip=skip,
        limit=limit,
        category=category,
        featured=featured,
        search=search,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/{skill_uuid}",
    response_model=SkillResponse,
    status_code=status.HTTP_200_OK,
)
async def get_skill(skill_uuid: UUID):
    return await SkillService.get_skill_by_uuid(skill_uuid)


# =========================================
# ADMIN ROUTES
# =========================================

@router.post(
    "/",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_skill(
    data: SkillCreate,
    current_admin: dict = Depends(admin_required),
):
    return await SkillService.create_skill(data)


@router.put(
    "/{skill_uuid}",
    response_model=SkillResponse,
    status_code=status.HTTP_200_OK,
)
async def update_skill(
    skill_uuid: UUID,
    data: SkillUpdate,
    current_admin: dict = Depends(admin_required),
):
    return await SkillService.update_skill(skill_uuid, data)


@router.delete(
    "/{skill_uuid}",
    status_code=status.HTTP_200_OK,
)
async def delete_skill(
    skill_uuid: UUID,
    current_admin: dict = Depends(admin_required),
):
    await SkillService.delete_skill(skill_uuid)
    return {"message": "Skill deleted successfully"}