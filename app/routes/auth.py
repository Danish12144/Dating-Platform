from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import auth as auth_schema
from app.core.firebase import verify_firebase_id_token
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.client import get_db
from app.models.user import User

router = APIRouter(tags=["auth"])
bearer_scheme = HTTPBearer()

@router.post("/auth/google", response_model=auth_schema.AuthSuccessResponse)
async def login_google(
    payload: auth_schema.GoogleLoginRequest,
    db=Depends(get_db)
):
    try:
        firebase_user = await verify_firebase_id_token(payload.idToken)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token") from exc

    uid = firebase_user["uid"]
    user = await User.get_by_firebase_uid(db, uid)

    if not user:
        new_user = {
            "firebase_uid": uid,
            "email": firebase_user.get("email"),
            "first_name": firebase_user.get("name", "User"),
            "phone": firebase_user.get("phone_number", ""),
            "status": "UNDER_REVIEW",
        }
        user = await User.create(db, new_user)

    user_id = str(user["_id"])
    access = create_access_token({"sub": user_id})
    refresh = create_refresh_token({"sub": user_id})

    # ✅ Refresh token DB mein save karo
    await User.update_profile(db, user_id, {"refresh_token": refresh})

    return {"success": True, "data": {"accessToken": access, "refreshToken": refresh}}


@router.post("/auth/refresh", response_model=auth_schema.AuthSuccessResponse)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db=Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)

    # ✅ Token type check
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user = await User.get_by_id(db, user_id)

    if not user or user.get("refresh_token") != token:
        raise HTTPException(status_code=401, detail="Token mismatch or user not found")

    # ✅ Naya token do
    new_access = create_access_token({"sub": user_id})
    new_refresh = create_refresh_token({"sub": user_id})
    await User.update_profile(db, user_id, {"refresh_token": new_refresh})

    return {"success": True, "data": {"accessToken": new_access, "refreshToken": new_refresh}}