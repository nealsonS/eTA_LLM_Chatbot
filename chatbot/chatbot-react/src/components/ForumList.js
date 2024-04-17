import React, { useState } from 'react';
import ForumItem from './ForumItem';

// Corrected import to load discussions from src/mockData.js
import { discussions } from '../mockData';  // Adjust the path as needed

function ForumList() {
    const [currentPage, setCurrentPage] = useState(1);
    const discussionsPerPage = 6;

    // Calculate the indices for slicing the discussion array
    const indexOfLastDiscussion = currentPage * discussionsPerPage;
    const indexOfFirstDiscussion = indexOfLastDiscussion - discussionsPerPage;
    const currentDiscussions = discussions.slice(indexOfFirstDiscussion, indexOfLastDiscussion);

    // Function to change page
    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    return (
        <div className="container">
            {currentDiscussions.map((discussion) => (
                <ForumItem key={discussion.id} data={discussion} />
            ))}
            <nav>
                <ul className='pagination justify-content-center'>
                    {Array.from({ length: Math.ceil(discussions.length / discussionsPerPage) }, (_, index) => (
                        <li key={index + 1} className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}>
                            <a onClick={() => paginate(index + 1)} className='page-link'>
                                {index + 1}
                            </a>
                        </li>
                    ))}
                </ul>
            </nav>
        </div>
    );
}

export default ForumList;
