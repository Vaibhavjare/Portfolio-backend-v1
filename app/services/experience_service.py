from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.experience import (
    Experience,
    ExperienceCreate,
    ExperienceUpdate
)


class ExperienceService:


    # ==============================
    # CREATE EXPERIENCE
    # ==============================

    @staticmethod
    async def create_experience(data: ExperienceCreate) -> Experience:

        experience = Experience(**data.model_dump())

        await experience.insert()

        return experience


    # ==============================
    # GET EXPERIENCES
    # ==============================

    @staticmethod
    async def get_experiences(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        featured: Optional[bool] = None
    ) -> List[Experience]:

        query = {}

        if search:
            query["company"] = {"$regex": search, "$options": "i"}

        if featured is not None:
            query["is_featured"] = featured

        return (
            await Experience.find(query)
            .sort("-start_date")
            .skip(skip)
            .limit(limit)
            .to_list()
        )


    # ==============================
    # GET EXPERIENCE BY UUID
    # ==============================

    @staticmethod
    async def get_experience_by_uuid(experience_uuid: UUID):

        return await Experience.find_one(
            Experience.experience_id == experience_uuid
        )


    # ==============================
    # UPDATE EXPERIENCE
    # ==============================

    @staticmethod
    async def update_experience(
        experience_uuid: UUID,
        data: ExperienceUpdate
    ):

        experience = await Experience.find_one(
            Experience.experience_id == experience_uuid
        )

        if not experience:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(experience, field, value)

        experience.updated_at = datetime.utcnow()

        await experience.save()

        return experience


    # ==============================
    # DELETE EXPERIENCE
    # ==============================

    @staticmethod
    async def delete_experience(experience_uuid: UUID):

        experience = await Experience.find_one(
            Experience.experience_id == experience_uuid
        )

        if not experience:
            return False

        await experience.delete()

        return True