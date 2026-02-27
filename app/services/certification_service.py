from datetime import datetime
from typing import List, Optional
from beanie import PydanticObjectId
from app.models.certification import (
    Certificate,
    CertificateCreate,
    CertificateUpdate,
)


class CertificateService:

    @staticmethod
    async def create_certificate(data: CertificateCreate) -> Certificate:
        certificate = Certificate(**data.model_dump())
        await certificate.insert()
        return certificate

    @staticmethod
    async def get_certificates(
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        featured: Optional[bool] = None,
    ) -> List[Certificate]:

        query = {}

        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        if featured is not None:
            query["is_featured"] = featured

        return await Certificate.find(query).skip(skip).limit(limit).to_list()

    @staticmethod
    async def get_certificate_by_id(certificate_id: str):
        return await Certificate.get(PydanticObjectId(certificate_id))

    @staticmethod
    async def update_certificate(
        certificate_id: str,
        data: CertificateUpdate,
    ):
        certificate = await Certificate.get(PydanticObjectId(certificate_id))

        if not certificate:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(certificate, field, value)

        certificate.updated_at = datetime.utcnow()

        await certificate.save()
        return certificate

    @staticmethod
    async def delete_certificate(certificate_id: str) -> bool:
        certificate = await Certificate.get(PydanticObjectId(certificate_id))

        if not certificate:
            return False

        await certificate.delete()
        return True