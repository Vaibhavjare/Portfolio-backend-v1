import logging
import certifi
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

from app.models.project_model import Project
from app.models.skill import Skill
from app.models.user_model import User
from app.models.certification import Certificate
from app.models.contact import Contact


logger = logging.getLogger("portfolio-db")

_client: Optional[AsyncIOMotorClient] = None


async def get_database():
    global _client

    if _client is None:
        _client = AsyncIOMotorClient(
            settings.MONGO_URL,
            tls=True,
            tlsCAFile=certifi.where(),  # 🔥 FIX SSL ISSUE
            serverSelectionTimeoutMS=10000,
        )

        logger.info("✅ MongoDB client initialized")

    return _client[settings.DATABASE_NAME]


async def init_db():
    db = await get_database()

    await init_beanie(
        database=db,
        document_models=[
            Project,
            Skill,
            User,
            Certificate,
            Contact,
        ],
    )

    logger.info("✅ Beanie initialized successfully")


async def close_db():
    global _client

    if _client:
        _client.close()
        logger.info("🔒 MongoDB connection closed")
        _client = None