// src/components/AssignmentCreate.jsx
import { useState } from 'react';
import { apiCreateAssignment } from '../api';

export default function AssignmentCreate({ token, onCreated }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [deadline, setDeadline] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      const resp = await apiCreateAssignment(token, { title, description, deadline: deadline || null });
      setTitle('');
      setDescription('');
      setDeadline('');
      onCreated(resp);
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <div className="card">
      <h3>Create Assignment</h3>
      {error && <p style={{color:'red'}}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} required />
        <textarea placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)} />
        <input type="datetime-local" value={deadline} onChange={e=>setDeadline(e.target.value)} />
        <button type="submit">Create</button>
      </form>
    </div>
  );
}