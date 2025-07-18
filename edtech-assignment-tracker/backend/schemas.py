# backend/schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class Role(str, Enum):
    teacher = "teacher"
    student = "student"


# ---------- Auth ----------
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


# ---------- Assignment ----------
class AssignmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class AssignmentOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Submission ----------
class SubmissionCreate(BaseModel):
    content: Optional[str] = None
    # file handled separately via multipart


class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    content: Optional[str]
    file_path: Optional[str]
    submitted_at: datetime

    class Config:
        from_attributes = True


# ---------- Aggregates ----------
class AssignmentWithSubs(AssignmentOut):
    submissions: List[SubmissionOut] = []