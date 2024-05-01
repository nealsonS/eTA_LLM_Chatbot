// src/components/LoginForm.js

import React, { useState } from 'react';

function LoginForm({ onUserLoggedIn }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:3800/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                onUserLoggedIn(data.user); // Notify parent component about the login
            } else {
                setErrorMessage(data.message || 'Login failed: Incorrect username or password');
            }
        } catch (error) {
            setErrorMessage('Network error: ' + error.message);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username</label>
                    <input type="text" className="form-control" id="username" required
                           value={username} onChange={e => setUsername(e.target.value)} />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" className="form-control" id="password" required
                           value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
            {errorMessage && <div className="alert alert-danger" role="alert">{errorMessage}</div>}
        </div>
    );
}

export default LoginForm;
