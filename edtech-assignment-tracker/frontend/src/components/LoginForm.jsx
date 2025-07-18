// src/components/LoginForm.jsx
import { useState } from 'react';
import { apiSignup, apiLogin, apiGetMe } from '../api';
import { saveToken } from '../auth';

export default function LoginForm({ onAuth }) {
  const [isSignup, setIsSignup] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student');
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    try {
      if (isSignup) {
        await apiSignup({ name, email, password, role });
      }
      const tokenResp = await apiLogin({ email, password });
      saveToken(tokenResp.access_token);
      const me = await apiGetMe(tokenResp.access_token);
      onAuth({ token: tokenResp.access_token, user: me });
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <div className="card">
      <h2>{isSignup ? 'Sign Up' : 'Log In'}</h2>
      {error && <p style={{color:'red'}}>{error}</p>}
      <form onSubmit={handleSubmit}>
        {isSignup && (
          <>
            <input placeholder="Full Name" value={name} onChange={e=>setName(e.target.value)} required />
            <select value={role} onChange={e=>setRole(e.target.value)}>
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
            </select>
          </>
        )}
        <input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} required />
        <button type="submit">{isSignup ? 'Create Account + Login' : 'Login'}</button>
      </form>
      <button onClick={()=>setIsSignup(!isSignup)}>
        {isSignup ? 'Have an account? Log in' : 'New user? Sign up'}
      </button>
    </div>
  );
}