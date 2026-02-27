from typing import List
from beanie import PydanticObjectId
from app.models.contact import (
    Contact,
    ContactCreate,
    ContactUpdate,
)


class ContactService:

    @staticmethod
    async def create_contact(data: ContactCreate) -> Contact:
        contact = Contact(**data.model_dump())
        await contact.insert()
        return contact

    @staticmethod
    async def get_contacts(skip: int = 0, limit: int = 20) -> List[Contact]:
        return await Contact.find_all().skip(skip).limit(limit).to_list()

    @staticmethod
    async def get_contact_by_id(contact_id: str):
        return await Contact.get(PydanticObjectId(contact_id))

    @staticmethod
    async def update_contact(contact_id: str, data: ContactUpdate):
        contact = await Contact.get(PydanticObjectId(contact_id))

        if not contact:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(contact, field, value)

        await contact.save()
        return contact

    @staticmethod
    async def delete_contact(contact_id: str) -> bool:
        contact = await Contact.get(PydanticObjectId(contact_id))

        if not contact:
            return False

        await contact.delete()
        return True