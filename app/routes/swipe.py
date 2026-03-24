# app/routes/swipe.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.client import get_db
from app.models.swipe import Swipe
from app.schemas import swipe as swipe_schema
from app.routes.users import get_current_user_id

router = APIRouter(tags=["swipe"])


@router.post("/swipe")
async def swipe(
    payload: swipe_schema.SwipeRequest,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    if payload.to_user_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot swipe yourself")
    if await Swipe.exists(db, from_user=user_id, to_user=payload.to_user_id):
        raise HTTPException(status_code=400, detail="Already swiped")
    await Swipe.create(db, from_user=user_id, to_user=payload.to_user_id, action=payload.action)
    return {"success": True, "message": "Swipe recorded"}
