import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ForumList from './components/ForumList';
import DiscussionDetail from './components/DiscussionDetail';
import NewDiscussionModal from './components/NewDiscussionModal';
import { discussions as initialDiscussions } from './mockData'; // Adjust import path as needed

function App() {
  const [discussions, setDiscussions] = useState(initialDiscussions);

  const addDiscussion = (newDiscussion) => {
    console.log("Adding discussion:", newDiscussion);  // Log to see the data
    setDiscussions(prevDiscussions => [...prevDiscussions, newDiscussion]);
    console.log("Updated discussions:", discussions);  // Log to see if state updates
  };

  return (
    <Router>
      <div className="App">
        <div className="container-fluid h-100">
          <div className="row h-100">
            <div className="col-md-4 mt-2">
              <div className='mt-2'>
                <ForumList discussions={discussions} />
              </div>
            </div>
            <div className="col-md-8 d-flex align-items-center justify-content-center">
              <Routes>
                <Route path="/" element={
                  <div className="text-center" style={{ maxWidth: "600px" }}>
                    <img src="/ETA.png" alt="Welcome" className="img-fluid" style={{ maxWidth: "200px" }} />
                    <h1>Welcome to the eTA Chatbot!</h1>
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
