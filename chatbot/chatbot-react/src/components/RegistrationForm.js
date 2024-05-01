// src/components/RegistrationForm.js

import React, { useState } from 'react';

function RegistrationForm({ onRegistrationSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:3800/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage('Registration successful! You can now log in.');
                onRegistrationSuccess();
            } else {
                setMessage('Registration failed: ' + data.message);
            }
        } catch (error) {
            setMessage('Network error: ' + error.message);
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
                <button type="submit" className="btn btn-success">Register</button>
            </form>
            {message && <div className="alert alert-info" role="alert">{message}</div>}
        </div>
    );
}

export default RegistrationForm;
