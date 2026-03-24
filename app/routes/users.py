# app/routes/users.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.core.security import decode_token
from app.db.client import get_db
from app.models.user import User
from app.schemas import user as user_schema

router = APIRouter(tags=["users"])


# ----- Helper: extract user id from JWT -----
async def get_current_user_id(Authorization: str = Depends(lambda: None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["sub"]


# ----- GET /users/me -----
@router.get("/users/me", response_model=user_schema.UserResponseSchema)
async def get_me(user_id: str = Depends(get_current_user_id), db=Depends(get_db)):
    user = await User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # calculate age
    dob = user["dob"]
    today = datetime.utcnow()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    user["age"] = age
    return user


# ----- PUT /users/me (profile update) -----
@router.put("/users/me", response_model=user_schema.UserResponseSchema)
async def update_profile(
    updates: user_schema.UserCreateSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    data = updates.dict(exclude_unset=True)
    updated = await User.update_profile(db, user_id, data)
    # recalc age
    dob = updated["dob"]
    today = datetime.utcnow()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    updated["age"] = age
    return updated


# ----- POST /users/location -----
@router.post("/users/location")
async def set_location(
    loc: user_schema.LocationSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    await User.update_profile(db, user_id, loc.dict())
    return {"success": True, "message": "Location saved"}


# ----- POST /users/preferences -----
@router.post("/users/preferences")
async def set_preferences(
    prefs: user_schema.PreferenceSchema,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    await User.update_profile(db, user_id, {"preferences": prefs.dict()})
    return {"success": True, "message": "Preferences saved"}
