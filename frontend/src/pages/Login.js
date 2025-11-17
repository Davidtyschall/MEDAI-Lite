import React, { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }

    setError('');
    onLogin(username);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="22" stroke="#667eea" strokeWidth="3"/>
              <path d="M24 12v24M12 24h24" stroke="#667eea" strokeWidth="3" strokeLinecap="round"/>
            </svg>
          </div>
          <h1>MEDAI-Lite</h1>
          <p>Health Risk Assessment Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && <div className="error">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              autoFocus
            />
          </div>

          <button type="submit" className="primary login-button">
            Continue as Guest
          </button>

          <div className="login-info">
            <p>ℹ️ This is a demo application. Enter any username to continue.</p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
