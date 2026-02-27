# app/routers/project_router.py

from fastapi import APIRouter, Query, Depends, status
from typing import List, Optional
from uuid import UUID

from app.models.project_model import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from app.services.project_service import ProjectService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# =========================================
# CREATE PROJECT (ADMIN ONLY)
# =========================================
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    data: ProjectCreate,
    _: dict = Depends(admin_required),
):
    return await ProjectService.create_project(data)


# =========================================
# GET PROJECTS (PUBLIC)
# =========================================
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    min_complexity: Optional[int] = Query(None, ge=1, le=10),
    max_complexity: Optional[int] = Query(None, ge=1, le=10),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    return await ProjectService.get_projects(
        skip=skip,
        limit=limit,
        search=search,
        featured=featured,
        min_complexity=min_complexity,
        max_complexity=max_complexity,
        sort_by=sort_by,
        order=order,
    )


# =========================================
# GET TOTAL COUNT (PUBLIC)
# =========================================
@router.get("/count", status_code=status.HTTP_200_OK)
async def get_project_count(
    search: Optional[str] = Query(None),
):
    total = await ProjectService.count_projects(search)
    return {"total": total}


# =========================================
# GET PROJECT BY UUID (PUBLIC)
# =========================================
@router.get("/{project_uuid}", response_model=ProjectResponse)
async def get_project_by_uuid(project_uuid: UUID):
    return await ProjectService.get_project_by_uuid(project_uuid)


# =========================================
# UPDATE PROJECT (ADMIN ONLY)
# =========================================
@router.put(
    "/{project_uuid}",
    response_model=ProjectResponse,
)
async def update_project(
    project_uuid: UUID,
    data: ProjectUpdate,
    _: dict = Depends(admin_required),
):
    return await ProjectService.update_project(project_uuid, data)


# =========================================
# DELETE PROJECT (ADMIN ONLY)
# =========================================
@router.delete(
    "/{project_uuid}",
    status_code=status.HTTP_200_OK,
)
async def delete_project(
    project_uuid: UUID,
    _: dict = Depends(admin_required),
):
    await ProjectService.delete_project(project_uuid)
    return {"message": "Project deleted successfully"}