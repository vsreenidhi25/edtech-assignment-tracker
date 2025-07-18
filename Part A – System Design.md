Part A – System Design
1. System Architecture (Simplified)
Frontend: React (or HTML/CSS/JS) – handles UI for student and teacher interactions.
Backend: FastAPI (Python) – handles API requests and business logic.
Database: PostgreSQL or SQLite – stores user, assignment, and submission data.
Authentication: JWT-based login with role-based access (Student or Teacher).

css
Copy
Edit
[Frontend] ⇄ [FastAPI Backend] ⇄ [Database]

2. Core Entities and Relationships
Entity	Attributes
User	id (PK), name, email, password (hashed), role (student/teacher)
Assignment	id (PK), title, description, deadline, teacher_id (FK to User)
Submission	id (PK), assignment_id (FK), student_id (FK), content, file_url, timestamp

Relationships:
One Teacher → Many Assignments
One Student → Many Submissions
One Assignment → Many Submissions

3. API Endpoints
Authentication APIs:
POST /signup – Create user (with role)
POST /login – Return JWT token
Teacher APIs:
POST /assignments – Create assignment (only teacher)
GET /assignments/{id}/submissions – View all submissions for a specific assignment

Student APIs:
POST /assignments/{id}/submit – Submit assignment (only student)

4. Authentication Strategy
Use JWT (JSON Web Tokens) for login sessions.
Protect routes based on user roles (middleware to verify teacher vs student).
On login, issue token with payload: { user_id, role }.
Use headers for subsequent requests: Authorization: Bearer <token>

5. Scalability Plan
Database Layer: Switch to PostgreSQL for production.
Caching: Use Redis to cache submissions or assignments for faster reads.
Load Balancing: Deploy behind Nginx or HAProxy for horizontal scaling.
File Storage: Use AWS S3 or equivalent for handling file uploads.
Microservices: Separate authentication, assignment, and submission into individual services as app grows.

