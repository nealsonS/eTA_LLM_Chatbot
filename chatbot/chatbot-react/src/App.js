// src/App.js

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ForumList from './components/ForumList';
import DiscussionDetail from './components/DiscussionDetail';
import NewDiscussionModal from './components/NewDiscussionModal';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';

function App() {
  const [discussions, setDiscussions] = useState([]);
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true); // Toggle between Login and Register
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false)


  useEffect(() => {
    const fetchDiscussions = async () => {
      const response = await fetch('http://localhost:3800/api/discussions');
      const data = await response.json();
      setDiscussions(data);
    };
    fetchDiscussions();
  },[]);


  const addDiscussion = async (newDiscussion) => {
    const response = await fetch('http://localhost:3800/api/discussions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newDiscussion)
    });
    const addedDiscussion = await response.json();
    setDiscussions(prevDiscussions => [addedDiscussion, ...prevDiscussions]);
  };

  const handleUserLoggedIn = (user) => {
    setIsLoggedIn(true);
    setUser(user)
    console.log('User logged in:', user);
  };

  const handleUserLoggedOut = () => {
    setIsLoggedIn(false);
    setUser(null)
    console.log('User logged out');
  };

  const handleRegistrationSuccess = () => {
    setShowLogin(true);
    console.log('Registration successful, switching to login');
  };


  return (
    <Router>
      <div className="App">
        <div className="container-fluid">
        {isLoggedIn ? (
          <div className="row align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
            <div className="col-md-4">
              <div className="m-3">
                <NewDiscussionModal addDiscussion={addDiscussion} />
              </div>
              <ForumList discussions={discussions} />
              <div className="fixed-bottom mb-3 ml-3">
                <button className="btn btn-danger" onClick={handleUserLoggedOut}>Logout</button>
              </div>
            </div>
            <div className="col-md-8 d-flex align-items-center justify-content-center">
              <Routes>
                <Route path="/" element={
                  <div className="text-center" style={{ maxWidth: "600px" }}>
                    <img src="/UF.png" alt="Welcome" className="img-fluid" style={{ maxWidth: "200px" }} />
                    <h1 style= {{color:'#faf3e6'}} >Welcome to UpAllNight Forums!</h1>
                    <p className="lead" style= {{color:'#faf3e6'}}>Click 'New Question' to ask a question or select a discussion to view details.</p>
                  </div>
                } />
                <Route path="/discussion/:id" element={<DiscussionDetail user={user} />} />
              </Routes>
            </div>
          </div>
        ) : (
          <div className="row align-items-center justify-content-center" style={{ minHeight: '100vh' }}>
            <div className="row-md-6 m-3">
              <div className='row align-items-center justify-content-center m-2'>
                <img src="/UF.png" alt="Welcome" className="img-fluid" style={{ maxWidth: "200px" }} />
              </div>
              <div>
                <h1 className="m-2 mb-4" style= {{color:'#faf3e6'}}>UpAllNight Forums</h1>
              </div>
              {showLogin ? (
                <LoginForm onUserLoggedIn={handleUserLoggedIn} />
              ) : (
                <RegistrationForm onRegistrationSuccess={handleRegistrationSuccess} />
              )}
              <button className="btn btn-link" onClick={() => setShowLogin(!showLogin)}>
                {showLogin ? 'Need an account? Register' : 'Already have an account? Login'}
              </button>
            </div>
          </div>
        )}
        </div>
      </div>
    </Router>
  );
}


export default App;
