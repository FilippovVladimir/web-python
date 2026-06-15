import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-env")
ALGORITHM = "HS256"
security = HTTPBearer()


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100_000,
    ).hex()
    return f"{salt}${password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    salt, expected_hash = stored_hash.split("$", 1)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100_000,
    ).hex()
    return hmac.compare_digest(password_hash, expected_hash)


def create_access_token(data: dict, minutes: int = 60) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    payload["exp"] = int(expire.timestamp())

    header_part = _b64_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_part = _b64_encode(json.dumps(payload, separators=(",", ":")).encode())
    message = f"{header_part}.{payload_part}".encode()
    signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
    return f"{header_part}.{payload_part}.{_b64_encode(signature)}"


def decode_access_token(token: str) -> dict | None:
    try:
        header_part, payload_part, signature_part = token.split(".")
        message = f"{header_part}.{payload_part}".encode()
        expected_signature = hmac.new(
            SECRET_KEY.encode(),
            message,
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(_b64_decode(signature_part), expected_signature):
            return None
        payload = json.loads(_b64_decode(payload_part))
        if payload["exp"] < int(datetime.now(timezone.utc).timestamp()):
            return None
        return payload
    except (ValueError, KeyError, json.JSONDecodeError):
        return None


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
