import React, { useState } from 'react';
import ForumItem from './ForumItem';
import { discussions } from '../mockData';  // Adjust the path as needed

function ForumList() {
    const [currentPage, setCurrentPage] = useState(1);
    const discussionsPerPage = 5;
    const totalPages = Math.ceil(discussions.length / discussionsPerPage);

    // Calculate the indices for slicing the discussion array
    const indexOfLastDiscussion = currentPage * discussionsPerPage;
    const indexOfFirstDiscussion = indexOfLastDiscussion - discussionsPerPage;
    const currentDiscussions = discussions.slice(indexOfFirstDiscussion, indexOfLastDiscussion);

    // Function to change page
    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    // Navigate to previous or next page
    const goToPrevPage = () => setCurrentPage(prev => Math.max(prev - 1, 1));
    const goToNextPage = () => setCurrentPage(prev => Math.min(prev + 1, totalPages));

    return (
        <div className="container">
            {currentDiscussions.map((discussion) => (
                <ForumItem key={discussion.id} data={discussion} />
            ))}
            <nav>
                <ul className='pagination justify-content-center'>
                    <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                        <a className='page-link' onClick={goToPrevPage}>
                            <i className="fas fa-chevron-left"></i>
                        </a>
                    </li>
                    {Array.from({ length: totalPages }, (_, index) => (
                        <li key={index + 1} className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}>
                            <a onClick={() => paginate(index + 1)} className='page-link'>
                                {index + 1}
                            </a>
                        </li>
                    ))}
                    <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                        <a className='page-link' onClick={goToNextPage}>
                            <i className="fas fa-chevron-right"></i>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default ForumList;
