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
        doc = await db[Message.collection_name].find_one({"_id": result.inserted_id})
        # ✅ ObjectId serialize karo
        doc["_id"] = str(doc["_id"])
        doc["from_user_id"] = str(doc["from_user_id"])
        doc["to_user_id"] = str(doc["to_user_id"])
        return doc

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
        msgs = await cursor.to_list(length=limit)
        # ✅ saare ObjectId serialize karo
        for m in msgs:
            m["_id"] = str(m["_id"])
            m["from_user_id"] = str(m["from_user_id"])
            m["to_user_id"] = str(m["to_user_id"])
        return msgs