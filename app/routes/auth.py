# app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import auth as auth_schema
from app.core.firebase import verify_firebase_id_token
from app.core.security import create_access_token, create_refresh_token
from app.db.client import get_db
from app.models.user import User

router = APIRouter(tags=["auth"])


@router.post("/auth/google", response_model=auth_schema.AuthSuccessResponse)
async def login_google(
    payload: auth_schema.GoogleLoginRequest,
    db=Depends(get_db)
):
    # Verify Firebase token
    try:
        firebase_user = await verify_firebase_id_token(payload.idToken)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        ) from exc

    uid = firebase_user["uid"]
    user = await User.get_by_firebase_uid(db, uid)

    if not user:
        # Minimal record – onboarding will fill the rest
        new_user = {
            "firebase_uid": uid,
            "email": firebase_user.get("email"),
            "first_name": firebase_user.get("name", "User"),
            "phone": firebase_user.get("phone_number", ""),
            "status": "UNDER_REVIEW",
        }
        user = await User.create(db, new_user)

    access = create_access_token({"sub": str(user["_id"])})
    refresh = create_refresh_token({"sub": str(user["_id"])})

    return {
        "success": True,
        "data": {
            "accessToken": access,
            "refreshToken": refresh,
        },
    }


@router.post("/auth/refresh", response_model=auth_schema.AuthSuccessResponse)
async def refresh_token():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh endpoint not implemented in MVP."
    )
