# app/utils/r2.py
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

def _get_r2_client():
    session = boto3.session.Session()
    client = session.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name=settings.R2_REGION,
    )
    return client


def generate_presigned_put_url(key: str, expires_in: int = 600) -> str:
    client = _get_r2_client()
    try:
        url = client.generate_presigned_url(
            "put_object",
            Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in,
        )
        return url
    except ClientError as exc:
        raise RuntimeError(f"Could not generate signed PUT URL: {exc}") from exc


def generate_presigned_get_url(key: str, expires_in: int = 600) -> str:
    client = _get_r2_client()
    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in,
        )
        return url
    except ClientError as exc:
        raise RuntimeError(f"Could not generate signed GET URL: {exc}") from exc
