# app/db/client.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

async def get_db():
    """FastAPI dependency – returns the DB object."""
    return db
