# app/routes/admin.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId
from app.db.client import get_db
from app.models.user import User
from app.schemas.admin import AdminActionSchema
from app.core.security import decode_token

router = APIRouter(tags=["admin"])


# ----- Admin guard (expects JWT with role="admin") -----
async def admin_required(Authorization: str = Depends(lambda: None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")
    try:
        scheme, token = Authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(status_code=401, detail="Bad Authorization header")
    payload = decode_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return payload["sub"]   # admin user id (optional)


# ----- GET /admin/users  (filterable) -----
@router.get("/admin/users")
async def list_users(
    status: str | None = Query(None),
    db=Depends(get_db),
    _: str = Depends(admin_required),
):
    filt = {}
    if status:
        filt["status"] = status
    cursor = db[User.collection_name].find(filt)
    users = await cursor.to_list(length=100)
    return {"success": True, "data": {"users": users}}


# ----- GET /admin/users/{id} -----
@router.get("/admin/users/{user_id}")
async def get_user_detail(
    user_id: str,
    db=Depends(get_db),
    _: str = Depends(admin_required),
):
    user = await User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": {"user": user}}


# ----- POST /admin/users/{id}/action -----
@router.post("/admin/users/{user_id}/action")
async def admin_action(
    user_id: str,
    action: AdminActionSchema,
    db=Depends(get_db),
    admin_id: str = Depends(admin_required),
):
    new_status = "APPROVED" if action.action == "APPROVE" else "REJECTED"
    await db[User.collection_name].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "status": new_status,
            "admin_note": {
                "reason": action.reason,
                "remark": action.remark,
                "by_admin": admin_id,
                "at": datetime.utcnow(),
            }
        }}
    )
    # TODO: send FCM notification about approval/rejection
    return {"success": True, "message": f"User {new_status.lower()}"}
