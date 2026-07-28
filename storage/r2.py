import os
from pathlib import Path
import boto3
from botocore.config import Config

from config import (
  R2_ACCESS_KEY_ID,
  R2_SECRET_ACCESS_KEY,
  R2_BUCKET_NAME,
  R2_ENDPOINT_URL,
  R2_ENABLED
)

def get_r2_client():
  if not R2_ENABLED:
    return None

  if not R2_ACCESS_KEY_ID or not R2_SECRET_ACCESS_KEY or not R2_ENDPOINT_URL:
    print("[R2] Warning: R2 credentials or endpoint URL missing.")
    return None

  return boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4")
  )

def upload_file(file_path: str, object_key: str | None = None) -> dict:
  if not R2_ENABLED:
    return {
      "success": False,
      "message": "R2 upload is disabled"
    }

  path = Path(file_path)
  if not path.exists():
    return {
      "success": False,
      "message": f"Local file not found: {file_path}"
    }

  key = object_key or path.name

  try:
    client = get_r2_client()
    if not client:
      return {
        "success": False,
        "message": "R2 client initialization failed"
      }

    print(f"[R2] Uploading {path.name} to bucket '{R2_BUCKET_NAME}' as '{key}'...")
    client.upload_file(
      str(path),
      R2_BUCKET_NAME,
      key
    )
    print(f"[R2] Upload successfully completed: {key}")

    return {
      "success":    True,
      "bucket":     R2_BUCKET_NAME,
      "object_key": key,
      "message":    "Uploaded to R2 successfully"
    }
  except Exception as e:
    err_msg = f"R2 upload error: {str(e)}"
    print(f"[R2] {err_msg}")
    return {
      "success": False,
      "message": err_msg
    }
