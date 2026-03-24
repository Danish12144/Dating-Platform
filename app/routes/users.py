from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user_id  # ✅ central import
from app.db.client import get_db
from app.models.user import User
from app.schemas import user as user_schema

router = APIRouter(tags=["users"])

def calc_age(dob) -> int | None:
    if not dob:
        return None
    today = datetime.utcnow()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@router.get("/users/me", response_model=user_schema.UserResponseSchema)
async def get_me(user_id: str = Depends(get_current_user_id), db=Depends(get_db)):
    user = await User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["age"] = calc_age(user.get("dob"))  # ✅ null safe
    return user

@router.put("/users/me", response_model=user_schema.UserResponseSchema)
async def update_profile(
    updates: user_schema.UserCreateSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    data = updates.dict(exclude_unset=True)
    updated = await User.update_profile(db, user_id, data)
    updated["age"] = calc_age(updated.get("dob"))  # ✅ null safe
    return updated

@router.post("/users/location")
async def set_location(
    loc: user_schema.LocationSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    await User.update_profile(db, user_id, loc.dict())
    return {"success": True, "message": "Location saved"}

@router.post("/users/preferences")
async def set_preferences(
    prefs: user_schema.PreferenceSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    await User.update_profile(db, user_id, {"preferences": prefs.dict()})
    return {"success": True, "message": "Preferences saved"}