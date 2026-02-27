# user_service.py

from datetime import datetime
from fastapi import HTTPException, UploadFile, status
from uuid import UUID

from app.models.user_model import User, UserProfileUpdate, UserRole
from app.core.google_drive import upload_file_to_drive


class UserService:

    # =========================================
    # INTERNAL HELPER - GET USER BY UUID
    # =========================================
    @staticmethod
    async def _get_user_by_uuid(user_id: str) -> User:
        try:
            uuid_obj = UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID",
            )

        user = await User.find_one(User.user_id == uuid_obj)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user


    # =========================================
    # GET PUBLIC PROFILE
    # =========================================
    @staticmethod
    async def get_public_profile():

        user = await User.find_one(User.role == UserRole.ADMIN)

        if not user or not getattr(user, "is_public", False):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        return user


    # =========================================
    # UPDATE FULL PROFILE (TEXT DATA)
    # =========================================
    @staticmethod
    async def update_profile(user_id: str, data: UserProfileUpdate):

        user = await UserService._get_user_by_uuid(user_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        await user.save()

        return user


    # =========================================
    # UPDATE PROFILE PHOTO
    # =========================================
    @staticmethod
    async def update_profile_photo(user_id: str, file: UploadFile):

        user = await UserService._get_user_by_uuid(user_id)

        photo_url = await upload_file_to_drive(
            file=file,
            filename=f"profile_{user.user_id}.jpg",
            subfolder="Profile-Photos",
        )

        user.profile_photo = photo_url
        user.updated_at = datetime.utcnow()
        await user.save()

        return user


    # =========================================
    # UPDATE RESUME
    # =========================================
    @staticmethod
    async def update_resume(user_id: str, file: UploadFile):

        user = await UserService._get_user_by_uuid(user_id)

        resume_url = await upload_file_to_drive(
            file=file,
            filename=f"resume_{user.user_id}.pdf",
            subfolder="Resumes",
        )

        user.resume_url = resume_url
        user.updated_at = datetime.utcnow()
        await user.save()

        return user


    # =========================================
    # UPDATE COVER IMAGE
    # =========================================
    @staticmethod
    async def update_cover_image(user_id: str, file: UploadFile):

        user = await UserService._get_user_by_uuid(user_id)

        cover_url = await upload_file_to_drive(
            file=file,
            filename=f"cover_{user.user_id}.jpg",
            subfolder="Cover-Images",
        )

        user.cover_image = cover_url
        user.updated_at = datetime.utcnow()
        await user.save()

        return user