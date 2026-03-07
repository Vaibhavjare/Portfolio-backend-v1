from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.education import (
    Education,
    EducationCreate,
    EducationUpdate
)


class EducationService:


    # ==============================
    # CREATE EDUCATION
    # ==============================

    @staticmethod
    async def create_education(data: EducationCreate) -> Education:

        education = Education(**data.model_dump())

        await education.insert()

        return education


    # ==============================
    # GET EDUCATIONS
    # ==============================

    @staticmethod
    async def get_educations(
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None
    ) -> List[Education]:

        query = {}

        if featured is not None:
            query["is_featured"] = featured

        return (
            await Education.find(query)
            .sort("-start_date")
            .skip(skip)
            .limit(limit)
            .to_list()
        )


    # ==============================
    # GET BY UUID
    # ==============================

    @staticmethod
    async def get_education_by_uuid(education_uuid: UUID):

        return await Education.find_one(
            Education.education_id == education_uuid
        )


    # ==============================
    # UPDATE EDUCATION
    # ==============================

    @staticmethod
    async def update_education(
        education_uuid: UUID,
        data: EducationUpdate
    ):

        education = await Education.find_one(
            Education.education_id == education_uuid
        )

        if not education:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(education, field, value)

        education.updated_at = datetime.utcnow()

        await education.save()

        return education


    # ==============================
    # DELETE EDUCATION
    # ==============================

    @staticmethod
    async def delete_education(education_uuid: UUID):

        education = await Education.find_one(
            Education.education_id == education_uuid
        )

        if not education:
            return False

        await education.delete()

        return True