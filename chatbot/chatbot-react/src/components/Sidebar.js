// src/components/Sidebar.js
import React, { useState } from 'react';

function Sidebar() {
  const [activeLink, setActiveLink] = useState('allThreads');

  const handleSetActive = (link) => {
    setActiveLink(link);
  };

  return (
    <div className="bg-white">
        <div className="inner-sidebar">
            <div className="inner-sidebar-body p-0">
                <div className="p-3 h-100" data-simplebar="init">
                    <nav className="nav nav-pills flex-column">
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'allThreads' ? 'active' : ''}`} onClick={() => handleSetActive('allThreads')}>All Threads</a>
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'popularWeek' ? 'active' : ''}`} onClick={() => handleSetActive('popularWeek')}>Popular this week</a>
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'popularAllTime' ? 'active' : ''}`} onClick={() => handleSetActive('popularAllTime')}>Popular all time</a>
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'solved' ? 'active' : ''}`} onClick={() => handleSetActive('solved')}>Solved</a>
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'unsolved' ? 'active' : ''}`} onClick={() => handleSetActive('unsolved')}>Unsolved</a>
                        <a href="#" className={`nav-link nav-link-faded has-icon ${activeLink === 'noReplies' ? 'active' : ''}`} onClick={() => handleSetActive('noReplies')}>No replies yet</a>
                    </nav>
                </div>
            </div>
        </div>
    </div>
  );
}

export default Sidebar;
