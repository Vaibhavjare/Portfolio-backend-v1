from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.blog import (
    Blog,
    BlogCreate,
    BlogUpdate
)


class BlogService:


    # ==============================
    # CREATE BLOG
    # ==============================

    @staticmethod
    async def create_blog(data: BlogCreate) -> Blog:

        blog = Blog(**data.model_dump())

        if blog.is_published:
            blog.published_at = datetime.utcnow()

        await blog.insert()

        return blog


    # ==============================
    # GET BLOGS
    # ==============================

    @staticmethod
    async def get_blogs(
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None,
        published: Optional[bool] = True
    ) -> List[Blog]:

        query = {}

        if published is not None:
            query["is_published"] = published

        if featured is not None:
            query["is_featured"] = featured

        return (
            await Blog.find(query)
            .sort("-published_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )


    # ==============================
    # GET BLOG BY UUID
    # ==============================

    @staticmethod
    async def get_blog_by_uuid(blog_uuid: UUID):

        return await Blog.find_one(
            Blog.blog_id == blog_uuid
        )


    # ==============================
    # UPDATE BLOG
    # ==============================

    @staticmethod
    async def update_blog(
        blog_uuid: UUID,
        data: BlogUpdate
    ):

        blog = await Blog.find_one(
            Blog.blog_id == blog_uuid
        )

        if not blog:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(blog, field, value)

        if "is_published" in update_data and update_data["is_published"]:
            blog.published_at = datetime.utcnow()

        blog.updated_at = datetime.utcnow()

        await blog.save()

        return blog


    # ==============================
    # DELETE BLOG
    # ==============================

    @staticmethod
    async def delete_blog(blog_uuid: UUID):

        blog = await Blog.find_one(
            Blog.blog_id == blog_uuid
        )

        if not blog:
            return False

        await blog.delete()

        return True