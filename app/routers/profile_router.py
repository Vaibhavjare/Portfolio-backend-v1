from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.models.user_model import (
    UserProfileUpdate,
    UserProfileResponse,
)
from app.services.user_service import UserService
from app.core.rbac import admin_required


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


# =========================================
# PUBLIC PROFILE VIEW
# =========================================
@router.get("/", response_model=UserProfileResponse)
async def get_profile():
    return await UserService.get_public_profile()


# =========================================
# ADMIN: UPDATE FULL PROFILE (TEXT DATA)
# =========================================
@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_profile(
    user_id: str,
    data: UserProfileUpdate,
    _=Depends(admin_required),
):
    return await UserService.update_profile(user_id, data)


# =========================================
# ADMIN: UPLOAD PROFILE PHOTO
# =========================================
@router.put("/{user_id}/profile-photo", response_model=UserProfileResponse)
async def update_profile_photo(
    user_id: str,
    file: UploadFile = File(...),
    _=Depends(admin_required),
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG and PNG allowed")

    return await UserService.update_profile_photo(user_id, file)


# =========================================
# ADMIN: UPLOAD RESUME (PDF)
# =========================================
@router.put("/{user_id}/resume", response_model=UserProfileResponse)
async def update_resume(
    user_id: str,
    file: UploadFile = File(...),
    _=Depends(admin_required),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    return await UserService.update_resume(user_id, file)


# =========================================
# ADMIN: UPLOAD COVER IMAGE
# =========================================
@router.put("/{user_id}/cover-image", response_model=UserProfileResponse)
async def update_cover_image(
    user_id: str,
    file: UploadFile = File(...),
    _=Depends(admin_required),
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG and PNG allowed")

    return await UserService.update_cover_image(user_id, file)