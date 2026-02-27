# app/services/skill_service.py

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pymongo import ASCENDING, DESCENDING
from fastapi import HTTPException, status

from app.models.skill import Skill, SkillCreate, SkillUpdate


class SkillService:

    # =========================================
    # CREATE SKILL
    # =========================================
    @staticmethod
    async def create_skill(data: SkillCreate) -> Skill:
        skill = Skill(**data.model_dump())
        await skill.insert()
        return skill


    # =========================================
    # GET SKILLS (Filter + Pagination)
    # =========================================
    @staticmethod
    async def get_skills(
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        featured: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: str = "display_order",
        order: str = "asc",
    ) -> List[Skill]:

        query: dict = {"is_active": True}

        if category:
            query["category"] = category

        if featured is not None:
            query["featured"] = featured

        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        # 🔒 Allowed sort fields (Security)
        allowed_sort_fields = {
            "display_order",
            "rating",
            "created_at",
            "updated_at",
            "name",
        }

        if sort_by not in allowed_sort_fields:
            sort_by = "display_order"

        sort_order = ASCENDING if order.lower() == "asc" else DESCENDING

        skills = (
            await Skill.find(query)
            .sort([(sort_by, sort_order)])
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return skills


    # =========================================
    # GET BY UUID (Public ID)
    # =========================================
    @staticmethod
    async def get_skill_by_uuid(skill_uuid: UUID) -> Skill:

        skill = await Skill.find_one(
            Skill.skill_id == skill_uuid,
            Skill.is_active == True,
        )

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )

        return skill


    # =========================================
    # UPDATE SKILL (BY UUID)
    # =========================================
    @staticmethod
    async def update_skill(
        skill_uuid: UUID,
        data: SkillUpdate,
    ) -> Skill:

        skill = await Skill.find_one(
            Skill.skill_id == skill_uuid,
            Skill.is_active == True,
        )

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(skill, field, value)

        skill.updated_at = datetime.utcnow()

        await skill.save()

        return skill


    # =========================================
    # DELETE SKILL (Soft Delete, BY UUID)
    # =========================================
    @staticmethod
    async def delete_skill(skill_uuid: UUID) -> bool:

        skill = await Skill.find_one(
            Skill.skill_id == skill_uuid,
            Skill.is_active == True,
        )

        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )

        skill.is_active = False
        skill.updated_at = datetime.utcnow()

        await skill.save()

        return True