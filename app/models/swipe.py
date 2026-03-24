# app/models/swipe.py
from datetime import datetime
from bson import ObjectId

class Swipe:
    collection_name = "swipes"

    @staticmethod
    async def create(db, from_user: str, to_user: str, action: str):
        doc = {
            "from_user": ObjectId(from_user),
            "to_user": ObjectId(to_user),
            "type": action,
            "created_at": datetime.utcnow(),
        }
        await db[Swipe.collection_name].insert_one(doc)
        return doc

    @staticmethod
    async def exists(db, from_user: str, to_user: str) -> bool:
        doc = await db[Swipe.collection_name].find_one({
            "from_user": ObjectId(from_user),
            "to_user": ObjectId(to_user)
        })
        return doc is not None
