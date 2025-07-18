
# 📘 EdTech Assignment Tracker – Fullstack App (FastAPI + React)

This project is a simplified **assignment tracking system** for an EdTech platform where:

- **Teachers** can post assignments and view submissions
- **Students** can submit their work

---

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python), SQLite (via SQLAlchemy)
- **Frontend**: React (Vite), Tailwind CSS (optional)
- **Auth**: JWT (with roles: `student`, `teacher`)

---

## ⚙️ Setup Instructions

### 🔧 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

> Make sure `main.py` is your FastAPI entry point. The app will run on `http://localhost:8000`.

---

### 💻 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

> This starts the frontend server on `http://localhost:5173`.

---

### 🗄️ 3. Database

- By default, uses SQLite: `sqlite:///./test.db`
- No manual setup required. Tables are auto-created by SQLAlchemy.
- To switch to PostgreSQL:
  - Install: `pip install psycopg2-binary`
  - Update `SQLALCHEMY_DATABASE_URL` in `database.py`

---

### 🔐 4. Authentication

- Auth is **role-based** (`student` or `teacher`)
- On login, backend returns a **JWT token**
- Include this token in all subsequent API requests:

```
Authorization: Bearer <your_token>
```

---


