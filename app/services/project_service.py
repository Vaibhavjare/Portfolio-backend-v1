# app/services/project_service.py

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pymongo import DESCENDING, ASCENDING
from fastapi import HTTPException, status

from app.models.project_model import Project, ProjectCreate, ProjectUpdate


class ProjectService:

    # =========================================
    # CREATE PROJECT
    # =========================================
    @staticmethod
    async def create_project(data: ProjectCreate) -> Project:
        project = Project(**data.model_dump())
        await project.insert()
        return project


    # =========================================
    # GET PROJECTS (Pagination + Filters)
    # =========================================
    @staticmethod
    async def get_projects(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        featured: Optional[bool] = None,
        min_complexity: Optional[int] = None,
        max_complexity: Optional[int] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> List[Project]:

        query: dict = {}

        # 🔍 Search by title (case-insensitive)
        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        # ⭐ Featured filter
        if featured is not None:
            query["featured"] = featured

        # 🎯 Complexity range filter
        if min_complexity is not None or max_complexity is not None:
            query["complexity_score"] = {}

            if min_complexity is not None:
                query["complexity_score"]["$gte"] = min_complexity

            if max_complexity is not None:
                query["complexity_score"]["$lte"] = max_complexity

        # 📌 Allowed sort fields (Security)
        allowed_sort_fields = {
            "created_at",
            "updated_at",
            "complexity_score",
            "title",
        }

        if sort_by not in allowed_sort_fields:
            sort_by = "created_at"

        sort_order = DESCENDING if order.lower() == "desc" else ASCENDING

        projects = (
            await Project.find(query)
            .sort([(sort_by, sort_order)])
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        return projects


    # =========================================
    # GET PROJECT BY UUID (PUBLIC SAFE ID)
    # =========================================
    @staticmethod
    async def get_project_by_uuid(project_uuid: UUID) -> Project:

        project = await Project.find_one(
            Project.project_id == project_uuid
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project


    # =========================================
    # UPDATE PROJECT (BY UUID)
    # =========================================
    @staticmethod
    async def update_project(
        project_uuid: UUID,
        data: ProjectUpdate,
    ) -> Project:

        project = await Project.find_one(
            Project.project_id == project_uuid
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        project.updated_at = datetime.utcnow()

        await project.save()

        return project


    # =========================================
    # DELETE PROJECT (BY UUID)
    # =========================================
    @staticmethod
    async def delete_project(project_uuid: UUID) -> bool:

        project = await Project.find_one(
            Project.project_id == project_uuid
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        await project.delete()

        return True


    # =========================================
    # COUNT PROJECTS
    # =========================================
    @staticmethod
    async def count_projects(search: Optional[str] = None) -> int:

        query: dict = {}

        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        return await Project.find(query).count()