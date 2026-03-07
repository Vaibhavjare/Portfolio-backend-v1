from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from app.models.education import (
    EducationCreate,
    EducationUpdate,
    EducationResponse
)

from app.services.education_service import EducationService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/educations",
    tags=["Educations"],
)


# ==============================
# PUBLIC - GET EDUCATIONS
# ==============================

@router.get("/", response_model=List[EducationResponse])
async def get_educations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    featured: Optional[bool] = None
):

    return await EducationService.get_educations(
        skip,
        limit,
        featured
    )


# ==============================
# GET SINGLE EDUCATION
# ==============================

@router.get("/{education_uuid}", response_model=EducationResponse)
async def get_education(education_uuid: UUID):

    education = await EducationService.get_education_by_uuid(
        education_uuid
    )

    if not education:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    return education


# ==============================
# ADMIN CREATE
# ==============================

@router.post("/", response_model=EducationResponse)
async def create_education(
    data: EducationCreate,
    _=Depends(admin_required)
):

    return await EducationService.create_education(data)


# ==============================
# ADMIN UPDATE
# ==============================

@router.put("/{education_uuid}", response_model=EducationResponse)
async def update_education(
    education_uuid: UUID,
    data: EducationUpdate,
    _=Depends(admin_required)
):

    education = await EducationService.update_education(
        education_uuid,
        data
    )

    if not education:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    return education


# ==============================
# ADMIN DELETE
# ==============================

@router.delete("/{education_uuid}")
async def delete_education(
    education_uuid: UUID,
    _=Depends(admin_required)
):

    deleted = await EducationService.delete_education(
        education_uuid
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Education not found"
        )

    return {"message": "Education deleted successfully"}