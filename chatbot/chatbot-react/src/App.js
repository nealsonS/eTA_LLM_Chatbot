import React from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import ForumList from './components/ForumList';
import NewDiscussionModal from './components/NewDiscussionModal';

function App() {
  return (
    <div className="App">
      <div className="container">
        <div className="row">
          <div className="col-lg-3">
            <NewDiscussionModal />
            <Sidebar />
          </div>
          <div className="col-lg-9">
            <ForumList />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
