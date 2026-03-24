# app/models/user.py
from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId

class User:
    collection_name = "users"

    @staticmethod
    async def create(db, data: dict) -> dict:
        data.update({
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "UNDER_REVIEW",
            "discover_enabled": True,
        })
        result = await db[User.collection_name].insert_one(data)
        return await db[User.collection_name].find_one({"_id": result.inserted_id})

    @staticmethod
    async def get_by_firebase_uid(db, uid: str) -> dict | None:
        return await db[User.collection_name].find_one({"firebase_uid": uid})

    @staticmethod
    async def get_by_id(db, user_id: str) -> dict | None:
        return await db[User.collection_name].find_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def update_profile(db, user_id: str, updates: dict) -> dict:
        updates["updated_at"] = datetime.utcnow()
        await db[User.collection_name].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updates}
        )
        return await User.get_by_id(db, user_id)

    @staticmethod
    async def list_for_discovery(
        db,
        current_user_id: str,
        location: Dict[str, float],
        prefs: dict,
        skip: int = 0,
        limit: int = 20,
    ) -> List[dict]:
        """
        Simple Euclidean distance filter (demo only). Production should use $geoNear.
        """
        lat, lng = location["latitude"], location["longitude"]
        max_km = prefs.get("distance_km", 50)
        age_min = prefs.get("age_min", 18)
        age_max = prefs.get("age_max", 100)

        today = datetime.utcnow()
        pipeline = [
            {"$match": {
                "_id": {"$ne": ObjectId(current_user_id)},
                "status": "APPROVED",
                "discover_enabled": True,
                "dob": {
                    "$gte": datetime(today.year - age_max, today.month, today.day),
                    "$lte": datetime(today.year - age_min, today.month, today.day)
                },
            }},
            # pseudo‑distance (not geospatially accurate)
            {"$addFields": {
                "distance_km": {
                    "$sqrt": {
                        "$add": [
                            {"$pow": [{"$subtract": ["$latitude", lat]}, 2]},
                            {"$pow": [{"$subtract": ["$longitude", lng]}, 2]},
                        ]
                    }
                }
            }},
            {"$match": {"distance_km": {"$lte": max_km}}},
            {"$skip": skip},
            {"$limit": limit},
        ]
        cursor = db[User.collection_name].aggregate(pipeline)
        return await cursor.to_list(length=limit)
