# backend/config.py
import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edtech.db")

# uploads
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.path.dirname(__file__), "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)