// src/App.jsx
import { useState } from 'react';
import LoginForm from './components/LoginForm';
import AssignmentCreate from './components/AssignmentCreate';
import AssignmentList from './components/AssignmentList';
import AssignmentSubmit from './components/AssignmentSubmit';
import SubmissionList from './components/SubmissionList';
import { clearToken } from './auth';

export default function App() {
  const [auth, setAuth] = useState(null); // {token, user}
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0); // trigger list refresh

  function handleLogout() {
    clearToken();
    setAuth(null);
  }

  function handleCreated() {
    // trigger assignment list refresh by changing key
    setRefreshKey(k => k + 1);
  }

  function handleSubmitted() {
    alert('Submission saved!');
  }

  if (!auth) {
    return (
      <div className="container">
        <LoginForm onAuth={setAuth} />
      </div>
    );
  }

  const { user, token } = auth;
  const isTeacher = user.role === 'teacher';
  const isStudent = user.role === 'student';

  return (
    <div className="container">
      <h1>EdTech Assignment Tracker</h1>
      <p>Logged in as {user.name} ({user.role}) <button onClick={handleLogout}>Logout</button></p>

      {isTeacher && <AssignmentCreate token={token} onCreated={handleCreated} />}

      {/* Key ensures reload when teacher creates new assignment */}
      <AssignmentList key={refreshKey} onSelect={setSelectedAssignment} />

      {selectedAssignment && isStudent && (
        <AssignmentSubmit token={token} assignment={selectedAssignment} onSubmitted={handleSubmitted} />
      )}

      {selectedAssignment && isTeacher && (
        <SubmissionList token={token} assignment={selectedAssignment} />
      )}
    </div>
  );
}