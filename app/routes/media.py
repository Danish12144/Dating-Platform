# app/routes/media.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.routes.users import get_current_user_id
from app.utils.r2 import generate_presigned_put_url, generate_presigned_get_url

router = APIRouter(tags=["media"])


@router.post("/media/upload-url")
async def get_upload_url(
    payload: dict = Body(..., example={"type": "photo", "slot": "V1"}),
    user_id: str = Depends(get_current_user_id),
):
    typ = payload.get("type")
    slot = payload.get("slot")
    if typ not in {"photo", "kyc"} or not slot:
        raise HTTPException(status_code=400, detail="Invalid payload")
    timestamp = int(datetime.utcnow().timestamp())
    key = f"users/{user_id}/{typ}/{slot}/{timestamp}"
    if typ == "photo":
        key = f"{key}.jpg"
    else:
        key = f"{key}.mp4"

    signed_url = generate_presigned_put_url(key)
    # In production you would also insert a document with status = PENDING
    return {"success": True, "data": {"upload_url": signed_url, "key": key}}


@router.get("/media/access-url")
async def get_access_url(
    key: str,
    user_id: str = Depends(get_current_user_id),
):
    # Very naive ownership check – only owner can fetch signed GET URL
    if not key.startswith(f"users/{user_id}/"):
        raise HTTPException(status_code=403, detail="Not allowed")
    url = generate_presigned_get_url(key)
    return {"success": True, "data": {"url": url}}
