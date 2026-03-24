# app/core/firebase.py
import firebase_admin
from firebase_admin import auth, credentials
from app.core.config import settings

def _build_firebase_cred():
    # Private key comes from .env with escaped \n, we need real newlines
    private_key = settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n")
    cred_dict = {
        "type": "service_account",
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": "placeholder",
        "private_key": private_key,
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": "placeholder",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "placeholder",
    }
    return credentials.Certificate(cred_dict)

if not firebase_admin._apps:   # avoid double init
    firebase_admin.initialize_app(_build_firebase_cred())

async def verify_firebase_id_token(id_token: str) -> dict:
    """
    Verifies Firebase ID token and returns decoded claims.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded
