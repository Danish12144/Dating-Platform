from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.db.client import get_db

bearer_scheme = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload["sub"]

async def get_current_active_user(
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db)
):
    from app.models.user import User
    user = await User.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.get("status") not in ("APPROVED",):
        raise HTTPException(status_code=403, detail="Account not approved yet")
    return user