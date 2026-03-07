from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional

from app.models.certification import (
    CertificateCreate,
    CertificateUpdate,
    CertificateResponse,
)
from app.services.certification_service import CertificateService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
)


# =========================================
# PUBLIC ROUTES
# =========================================

@router.get("/", response_model=List[CertificateResponse])
async def get_certificates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    featured: Optional[bool] = None,
):
    return await CertificateService.get_certificates(
        skip=skip,
        limit=limit,
        search=search,
        featured=featured,
    )


@router.get("/{certificate_id}", response_model=CertificateResponse)
async def get_certificate(certificate_id: str):
    certificate = await CertificateService.get_certificate_by_id(certificate_id)

    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    return certificate


# =========================================
# ADMIN ROUTES
# =========================================

@router.post("/", response_model=CertificateResponse)
async def create_certificate(
    data: CertificateCreate,
    _=Depends(admin_required),
):
    return await CertificateService.create_certificate(data)


@router.put("/{certificate_id}", response_model=CertificateResponse)
async def update_certificate(
    certificate_id: str,
    data: CertificateUpdate,
    _=Depends(admin_required),
):
    certificate = await CertificateService.update_certificate(
        certificate_id,
        data,
    )

    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    return certificate


@router.delete("/{certificate_id}")
async def delete_certificate(
    certificate_id: str,
    _=Depends(admin_required),
):
    deleted = await CertificateService.delete_certificate(certificate_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Certificate not found")

    return {"message": "Certificate deleted successfully"}  