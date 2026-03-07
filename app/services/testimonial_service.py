from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models.testimonial import (
    Testimonial,
    TestimonialCreate,
    TestimonialUpdate
)


class TestimonialService:


    # ==============================
    # CREATE TESTIMONIAL
    # ==============================

    @staticmethod
    async def create_testimonial(data: TestimonialCreate) -> Testimonial:

        testimonial = Testimonial(**data.model_dump())

        await testimonial.insert()

        return testimonial


    # ==============================
    # GET TESTIMONIALS
    # ==============================

    @staticmethod
    async def get_testimonials(
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None
    ) -> List[Testimonial]:

        query = {}

        if featured is not None:
            query["is_featured"] = featured

        return (
            await Testimonial.find(query)
            .sort("-created_at")
            .skip(skip)
            .limit(limit)
            .to_list()
        )


    # ==============================
    # GET BY UUID
    # ==============================

    @staticmethod
    async def get_testimonial_by_uuid(testimonial_uuid: UUID):

        return await Testimonial.find_one(
            Testimonial.testimonial_id == testimonial_uuid
        )


    # ==============================
    # UPDATE TESTIMONIAL
    # ==============================

    @staticmethod
    async def update_testimonial(
        testimonial_uuid: UUID,
        data: TestimonialUpdate
    ):

        testimonial = await Testimonial.find_one(
            Testimonial.testimonial_id == testimonial_uuid
        )

        if not testimonial:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(testimonial, field, value)

        testimonial.updated_at = datetime.utcnow()

        await testimonial.save()

        return testimonial


    # ==============================
    # DELETE TESTIMONIAL
    # ==============================

    @staticmethod
    async def delete_testimonial(testimonial_uuid: UUID):

        testimonial = await Testimonial.find_one(
            Testimonial.testimonial_id == testimonial_uuid
        )

        if not testimonial:
            return False

        await testimonial.delete()

        return True