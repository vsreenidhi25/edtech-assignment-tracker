# backend/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime

from . import models, schemas
from .utils import hash_password


# ----- Users -----
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserSignup) -> models.User:
    user = models.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=models.UserRole(user_in.role.value),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


# ----- Assignments -----
def create_assignment(db: Session, teacher_id: int, data: schemas.AssignmentCreate) -> models.Assignment:
    assign = models.Assignment(
        title=data.title,
        description=data.description,
        deadline=data.deadline,
        teacher_id=teacher_id,
    )
    db.add(assign)
    db.commit()
    db.refresh(assign)
    return assign


def list_assignments(db: Session) -> List[models.Assignment]:
    return db.query(models.Assignment).order_by(models.Assignment.created_at.desc()).all()


def get_assignment(db: Session, assignment_id: int) -> Optional[models.Assignment]:
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()


# ----- Submissions -----
def create_submission(db: Session, assignment_id: int, student_id: int, content: str = None, file_path: str = None) -> models.Submission:
    sub = models.Submission(
        assignment_id=assignment_id,
        student_id=student_id,
        content=content,
        file_path=file_path,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def get_submissions_for_assignment(db: Session, assignment_id: int) -> List[models.Submission]:
    return db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()


def get_submissions_for_student(db: Session, student_id: int) -> List[models.Submission]:
    return db.query(models.Submission).filter(models.Submission.student_id == student_id).all()