// src/components/SubmissionList.jsx
import { useEffect, useState } from 'react';
import { apiViewSubmissions } from '../api';

export default function SubmissionList({ token, assignment }) {
  const [subs, setSubs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!assignment) return;
    (async () => {
      try {
        const data = await apiViewSubmissions(token, assignment.id);
        setSubs(data);
      } catch (err) {
        setError(String(err));
      }
    })();
  }, [assignment, token]);

  return (
    <div className="card">
      <h3>Submissions for: {assignment.title}</h3>
      {error && <p style={{color:'red'}}>{error}</p>}
      {subs.length === 0 && <p>No submissions yet.</p>}
      {subs.map(s => (
        <div key={s.id} className="card" style={{border:'1px solid #ccc'}}>
          <p><strong>Student ID:</strong> {s.student_id}</p>
          {s.content && <p>{s.content}</p>}
          {s.file_path && <p className="small">File saved at server: {s.file_path}</p>}
          <p className="small">Submitted: {new Date(s.submitted_at).toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
}