from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List

from app.models.contact import (
    ContactCreate,
    ContactUpdate,
    ContactResponse,
)
from app.services.contact_service import ContactService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


# =========================================
# PUBLIC ROUTE (Submit Contact Form)
# =========================================

@router.post("/", response_model=ContactResponse)
async def create_contact(data: ContactCreate):
    return await ContactService.create_contact(data)


# =========================================
# ADMIN ROUTES
# =========================================

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _=Depends(admin_required),
):
    return await ContactService.get_contacts(skip, limit)


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: str,
    _=Depends(admin_required),
):
    contact = await ContactService.get_contact_by_id(contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    data: ContactUpdate,
    _=Depends(admin_required),
):
    contact = await ContactService.update_contact(contact_id, data)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: str,
    _=Depends(admin_required),
):
    deleted = await ContactService.delete_contact(contact_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted successfully"}