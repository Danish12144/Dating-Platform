# app/routes/discovery.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.db.client import get_db
from app.models.user import User
from app.core.dependencies import get_current_user_id
from app.utils.pagination import pagination_params

router = APIRouter(tags=["discovery"])


@router.get("/discovery")
async def discovery_feed(
    pagination: dict = Depends(pagination_params()),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    me = await User.get_by_id(db, user_id)
    if not me:
        raise HTTPException(status_code=404, detail="User not found")

    location = {"latitude": me.get("latitude"), "longitude": me.get("longitude")}
    if not location["latitude"] or not location["longitude"]:
        raise HTTPException(status_code=400, detail="Location not set")

    prefs = me.get("preferences", {})
    users = await User.list_for_discovery(
        db,
        current_user_id=user_id,
        location=location,
        prefs=prefs,
        skip=pagination["skip"],
        limit=pagination["limit"],
    )

    result = []
    for u in users:
        dob = u.get("dob")
        if not dob:
            continue  # ✅ null safe
        today = datetime.utcnow()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        result.append({
            "id": str(u["_id"]),
            "first_name": u["first_name"],
            "age": age,
            "city": u.get("city", ""),
            "distance_km": round(u.get("distance_km", 0), 2),
            "photos": u.get("photos", []),
        })

    return {"success": True, "data": {"users": result}}