// src/App.js

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ForumList from './components/ForumList';
import DiscussionDetail from './components/DiscussionDetail';
import NewDiscussionModal from './components/NewDiscussionModal';

function App() {
  const [discussions, setDiscussions] = useState([]);

  useEffect(() => {
    const fetchDiscussions = async () => {
      const response = await fetch('http://localhost:3800/api/discussions');
      const data = await response.json();
      setDiscussions(data);
    };
    fetchDiscussions();
  }, []);

  const addDiscussion = async (newDiscussion) => {
    const response = await fetch('http://localhost:3800/api/discussions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newDiscussion)
    });
    const addedDiscussion = await response.json();
    setDiscussions(prevDiscussions => [ addedDiscussion, ...prevDiscussions]);
  };

  return (
    <Router>
      <div className="App">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-4">
              <div className="m-3">
              <NewDiscussionModal addDiscussion={addDiscussion} />
              </div>
              <ForumList discussions={discussions} />
            </div>
            <div className="col-md-8 d-flex align-items-center justify-content-center">
              <Routes>
                <Route path="/" element={
                  <div className="text-center" style={{ maxWidth: "600px" }}>
                    <img src="/ETA.png" alt="Welcome" className="img-fluid" style={{ maxWidth: "200px" }} />
                    <h1>Welcome to UpAllNight Forums!</h1>
                    <p className="lead">Click 'New Question' to ask a question</p>
                    <p className="lead">or select a discussion to view details.</p>
                  </div>
                } />
                <Route path="/discussion/:id" element={<DiscussionDetail />} />
              </Routes>
            </div>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
