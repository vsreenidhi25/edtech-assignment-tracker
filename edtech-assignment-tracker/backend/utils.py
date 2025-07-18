# backend/utils.py
import os
import uuid
from passlib.context import CryptContext
from .config import UPLOAD_DIR

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def save_upload_file(upload_file, subdir: str = "") -> str:
    # Returns server-side file path
    ext = os.path.splitext(upload_file.filename)[1]
    fname = f"{uuid.uuid4().hex}{ext}"
    target_dir = os.path.join(UPLOAD_DIR, subdir)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, fname)
    with open(target_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return target_path