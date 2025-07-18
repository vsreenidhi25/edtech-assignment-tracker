# backend/main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from . import models, schemas, crud
from .database import engine, get_db
from .utils import verify_password, save_upload_file
from .auth import create_access_token
from .deps import get_current_user, require_teacher, require_student

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EdTech Assignment Tracker", version="0.1.0")

# CORS (allow localhost dev by default)
origins = [
    "http://localhost",
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Auth Endpoints ----------
@app.post("/signup", response_model=schemas.UserBase, status_code=201)
def signup(user_in: schemas.UserSignup, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, user_in)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has username & password fields
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token({"sub": user.id, "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.UserBase)
def read_current_user(user=Depends(get_current_user)):
    return user


# ---------- Assignment Endpoints ----------
@app.post("/assignments", response_model=schemas.AssignmentOut, status_code=201)
def create_assignment(
    assignment_in: schemas.AssignmentCreate,
    teacher=Depends(require_teacher),
    db: Session = Depends(get_db),
):
    return crud.create_assignment(db, teacher_id=teacher.id, data=assignment_in)


@app.get("/assignments", response_model=List[schemas.AssignmentOut])
def list_all_assignments(db: Session = Depends(get_db)):
    return crud.list_assignments(db)


@app.get("/assignments/{assignment_id}", response_model=schemas.AssignmentOut)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


# ---------- Submission Endpoints ----------
@app.post("/assignments/{assignment_id}/submit", response_model=schemas.SubmissionOut, status_code=201)
async def submit_assignment(
    assignment_id: int,
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    student=Depends(require_student),
    db: Session = Depends(get_db),
):
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    file_path = None
    if file is not None:
        file_path = save_upload_file(file, subdir=str(assignment_id))

    sub = crud.create_submission(db, assignment_id, student.id, content, file_path)
    return sub


@app.get("/assignments/{assignment_id}/submissions", response_model=List[schemas.SubmissionOut])
def view_submissions(
    assignment_id: int,
    teacher=Depends(require_teacher),
    db: Session = Depends(get_db),
):
    assignment = crud.get_assignment(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # (Optional) restrict to teacher's own assignments
    if assignment.teacher_id != teacher.id:
        raise HTTPException(status_code=403, detail="Not your assignment")

    return crud.get_submissions_for_assignment(db, assignment_id)


# Optional convenience route: student views own submissions
@app.get("/my-submissions", response_model=List[schemas.SubmissionOut])
def my_submissions(student=Depends(require_student), db: Session = Depends(get_db)):
    return crud.get_submissions_for_student(db, student.id)