// src/components/RegistrationForm.js

import React, { useState } from 'react';

function RegistrationForm({ onRegistrationSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isTA, setIsTA] = useState(false);
    const [verificationCode, setVerificationCode] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:3800/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, isTA, verificationCode })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage('Registration successful! Switching to log in...');
                setTimeout(() => {
                    onRegistrationSuccess();
                }, 1300);
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
                    <label htmlFor="username" style= {{color:'#faf3e6'}}>Username</label>
                    <input type="text" className="form-control" id="username" required
                           value={username} onChange={e => setUsername(e.target.value)} />
                </div>
                <div className="form-group">
                    <label htmlFor="password" style= {{color:'#faf3e6'}}>Password</label>
                    <input type="password" className="form-control" id="password" required
                           value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <div className="form-check">
                    <input type="checkbox" className="form-check-input" id="isTA" checked={isTA} onChange={e => setIsTA(e.target.checked)} />
                    <label className="form-check-label" htmlFor="isTA" style= {{color:'#faf3e6'}}>Are you a TA?</label>
                </div>
                {isTA && (
                    <div className="form-group">
                        <label htmlFor="verificationCode" style= {{color:'#faf3e6'}}>Verification Code</label>
                        <input type="text" className="form-control" id="verificationCode" required value={verificationCode} onChange={e => setVerificationCode(e.target.value)} />
                    </div>
                )}
                <button type="submit" className="btn btn-success mt-2">Register</button>
            </form>
            {message && <div className="alert alert-info" role="alert">{message}</div>}
        </div>
    );
}

export default RegistrationForm;
