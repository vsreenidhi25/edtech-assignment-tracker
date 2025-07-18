// src/api.js
const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

export async function apiSignup({ name, email, password, role }) {
  const res = await fetch(`${API_BASE}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password, role })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiLogin({ email, password }) {
  const formData = new FormData();
  formData.append('username', email); // OAuth2PasswordRequestForm expects 'username'
  formData.append('password', password);

  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiGetMe(token) {
  const res = await fetch(`${API_BASE}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiCreateAssignment(token, { title, description, deadline }) {
  const res = await fetch(`${API_BASE}/assignments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, description, deadline })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiListAssignments() {
  const res = await fetch(`${API_BASE}/assignments`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiSubmitAssignment(token, assignmentId, { content, file }) {
  const formData = new FormData();
  if (content) formData.append('content', content);
  if (file) formData.append('file', file);

  const res = await fetch(`${API_BASE}/assignments/${assignmentId}/submit`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiViewSubmissions(token, assignmentId) {
  const res = await fetch(`${API_BASE}/assignments/${assignmentId}/submissions`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}