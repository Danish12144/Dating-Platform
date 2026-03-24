# app/models/chat.py
from datetime import datetime
from bson import ObjectId
from typing import List

class Message:
    collection_name = "messages"

    @staticmethod
    async def send(db, from_user: str, to_user: str, content: str | None, media_url: str | None):
        doc = {
            "from_user_id": ObjectId(from_user),
            "to_user_id": ObjectId(to_user),
            "content": content,
            "media_url": media_url,
            "created_at": datetime.utcnow(),
        }
        result = await db[Message.collection_name].insert_one(doc)
        return await db[Message.collection_name].find_one({"_id": result.inserted_id})

    @staticmethod
    async def get_conversation(
        db,
        user_a: str,
        user_b: str,
        skip: int = 0,
        limit: int = 20,
    ) -> List[dict]:
        cursor = db[Message.collection_name].find({
            "$or": [
                {"from_user_id": ObjectId(user_a), "to_user_id": ObjectId(user_b)},
                {"from_user_id": ObjectId(user_b), "to_user_id": ObjectId(user_a)},
            ]
        }).sort("created_at", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
