# backend/models.py
from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


class UserRole(str, enum.Enum):
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    assignments = relationship("Assignment", back_populates="teacher")
    submissions = relationship("Submission", back_populates="student")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"))
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)  # server-side path to uploaded file
    submitted_at = Column(DateTime, default=datetime.utcnow)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", back_populates="submissions")