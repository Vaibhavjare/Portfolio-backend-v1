from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID

from app.models.testimonial import (
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialResponse
)

from app.services.testimonial_service import TestimonialService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/testimonials",
    tags=["Testimonials"],
)


# ==============================
# PUBLIC GET
# ==============================

@router.get("/", response_model=List[TestimonialResponse])
async def get_testimonials(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    featured: Optional[bool] = None
):

    return await TestimonialService.get_testimonials(
        skip,
        limit,
        featured
    )


# ==============================
# GET SINGLE
# ==============================

@router.get("/{testimonial_uuid}", response_model=TestimonialResponse)
async def get_testimonial(testimonial_uuid: UUID):

    testimonial = await TestimonialService.get_testimonial_by_uuid(
        testimonial_uuid
    )

    if not testimonial:
        raise HTTPException(
            status_code=404,
            detail="Testimonial not found"
        )

    return testimonial


# ==============================
# ADMIN CREATE
# ==============================

@router.post("/", response_model=TestimonialResponse)
async def create_testimonial(
    data: TestimonialCreate,
    _=Depends(admin_required)
):

    return await TestimonialService.create_testimonial(data)


# ==============================
# ADMIN UPDATE
# ==============================

@router.put("/{testimonial_uuid}", response_model=TestimonialResponse)
async def update_testimonial(
    testimonial_uuid: UUID,
    data: TestimonialUpdate,
    _=Depends(admin_required)
):

    testimonial = await TestimonialService.update_testimonial(
        testimonial_uuid,
        data
    )

    if not testimonial:
        raise HTTPException(
            status_code=404,
            detail="Testimonial not found"
        )

    return testimonial


# ==============================
# ADMIN DELETE
# ==============================

@router.delete("/{testimonial_uuid}")
async def delete_testimonial(
    testimonial_uuid: UUID,
    _=Depends(admin_required)
):

    deleted = await TestimonialService.delete_testimonial(
        testimonial_uuid
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Testimonial not found"
        )

    return {"message": "Testimonial deleted successfully"}
