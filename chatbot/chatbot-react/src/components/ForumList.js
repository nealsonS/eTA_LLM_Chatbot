import React, { useState } from 'react';
import ForumItem from './ForumItem';
import NewDiscussionModal from './NewDiscussionModal'; // Ensure this is properly imported

function ForumList({ discussions }) {
    const [currentPage, setCurrentPage] = useState(1);
    const discussionsPerPage = 5; // Adjust this if needed
    const totalPages = Math.ceil(discussions.length / discussionsPerPage);
    const indexOfLastDiscussion = currentPage * discussionsPerPage;
    const indexOfFirstDiscussion = indexOfLastDiscussion - discussionsPerPage;
    // src/components/ForumList.js

    const currentDiscussions = discussions.slice(indexOfFirstDiscussion, indexOfLastDiscussion);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);
    const goToPrevPage = () => setCurrentPage(prev => Math.max(prev - 1, 1));
    const goToNextPage = () => setCurrentPage(prev => Math.min(prev + 1, totalPages));

    return (
        <div className="container">
            {/* <div className="mb-3">
                <NewDiscussionModal />
            </div> */}
            {currentDiscussions.map((discussion) => (
                <ForumItem key={discussion.id} data={discussion} />
            ))}
            <nav>
                <ul className='pagination justify-content-center'>
                    <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                        <button className='page-link' onClick={goToPrevPage}>
                            <i className="fas fa-chevron-left"></i>
                        </button>
                    </li>
                    {Array.from({ length: totalPages }, (_, index) => (
                        <li key={index + 1} className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}>
                            <button onClick={() => paginate(index + 1)} className='page-link'>
                                {index + 1}
                            </button>
                        </li>
                    ))}
                    <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                        <button className='page-link' onClick={goToNextPage}>
                            <i className="fas fa-chevron-right"></i>
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default ForumList;
