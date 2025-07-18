// src/components/AssignmentSubmit.jsx
import { useState } from 'react';
import { apiSubmitAssignment } from '../api';

export default function AssignmentSubmit({ token, assignment, onSubmitted }) {
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      const resp = await apiSubmitAssignment(token, assignment.id, { content, file });
      setContent('');
      setFile(null);
      onSubmitted(resp);
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <div className="card">
      <h3>Submit: {assignment.title}</h3>
      {error && <p style={{color:'red'}}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <textarea placeholder="Submission content" value={content} onChange={e=>setContent(e.target.value)} />
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}