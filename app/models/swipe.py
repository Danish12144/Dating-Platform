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

    @staticmethod
    async def check_match(db, user_a: str, user_b: str) -> bool:
        # ✅ Check karo kya user_b ne bhi user_a ko LIKE kiya hai
        doc = await db[Swipe.collection_name].find_one({
            "from_user": ObjectId(user_b),
            "to_user": ObjectId(user_a),
            "type": "LIKE"
        })
        return doc is not None