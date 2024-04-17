// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ForumList from './components/ForumList';
import DiscussionDetail from './components/DiscussionDetail';
import NewDiscussionModal from './components/NewDiscussionModal';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="container">
          <div className="row">
            <div className="col-lg-3">
              <NewDiscussionModal />
              <Sidebar />
            </div>
            <div className="col-lg-9">
              <Routes>
                <Route path="/" element={<ForumList />} />
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
