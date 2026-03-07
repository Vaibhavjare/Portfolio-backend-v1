from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.achievement import (
    Achievement,
    AchievementCreate,
    AchievementUpdate
)


class AchievementService:


    # ==============================
    # CREATE ACHIEVEMENT
    # ==============================

    @staticmethod
    async def create_achievement(data: AchievementCreate) -> Achievement:

        achievement = Achievement(**data.model_dump())

        await achievement.insert()

        return achievement


    # ==============================
    # GET ACHIEVEMENTS
    # ==============================

    @staticmethod
    async def get_achievements(
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None
    ) -> List[Achievement]:

        query = {}

        if featured is not None:
            query["is_featured"] = featured

        return (
            await Achievement.find(query)
            .sort("-achievement_date")
            .skip(skip)
            .limit(limit)
            .to_list()
        )


    # ==============================
    # GET BY UUID
    # ==============================

    @staticmethod
    async def get_achievement_by_uuid(achievement_uuid: UUID):

        return await Achievement.find_one(
            Achievement.achievement_id == achievement_uuid
        )


    # ==============================
    # UPDATE ACHIEVEMENT
    # ==============================

    @staticmethod
    async def update_achievement(
        achievement_uuid: UUID,
        data: AchievementUpdate
    ):

        achievement = await Achievement.find_one(
            Achievement.achievement_id == achievement_uuid
        )

        if not achievement:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(achievement, field, value)

        achievement.updated_at = datetime.utcnow()

        await achievement.save()

        return achievement


    # ==============================
    # DELETE ACHIEVEMENT
    # ==============================

    @staticmethod
    async def delete_achievement(achievement_uuid: UUID):

        achievement = await Achievement.find_one(
            Achievement.achievement_id == achievement_uuid
        )

        if not achievement:
            return False

        await achievement.delete()

        return True