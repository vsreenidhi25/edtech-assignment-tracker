// src/components/AssignmentList.jsx
import { useEffect, useState } from 'react';
import { apiListAssignments } from '../api';

export default function AssignmentList({ onSelect }) {
  const [assignments, setAssignments] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const data = await apiListAssignments();
        setAssignments(data);
      } catch (err) {
        setError(String(err));
      }
    })();
  }, []);

  return (
    <div className="card">
      <h3>Assignments</h3>
      {error && <p style={{color:'red'}}>{error}</p>}
      {assignments.map(a => (
        <div key={a.id} className="card" style={{border:'1px solid #ccc'}}>
          <h4>{a.title}</h4>
          <p>{a.description}</p>
          {a.deadline && <p className="small">Deadline: {new Date(a.deadline).toLocaleString()}</p>}
          <button onClick={()=>onSelect(a)}>Open</button>
        </div>
      ))}
    </div>
  );
}