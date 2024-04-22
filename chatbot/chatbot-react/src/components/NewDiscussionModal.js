// src/components/NewDiscussionModal.js

import React, { useState } from 'react';

function NewDiscussionModal({ addDiscussion }) {
    const [isOpen, setIsOpen] = useState(false);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const toggleModal = () => setIsOpen(!isOpen);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Create a new discussion object
        const newDiscussion = {
            title: title,
            content: content,
            user: 'Student',
            avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
            replyTime: 'Just now',
            views: 0,
            comments: []
        };
        addDiscussion(newDiscussion);  // Add the new discussion to the list
        setTitle('');  // Reset title
        setContent('');  // Reset content
        toggleModal();  // Close modal
    };

    return (
        <>
            <button 
                className="btn btn-primary btn-lg btn-block shadow-sm"
                style={{
                    borderRadius: '0.5rem', // Rounded corners
                    border: 'none',         // Remove default border
                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' // Subtle shadow for depth
                }}
                onClick={toggleModal}>+ New Question
            </button>
            {isOpen && (
                <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1" role="dialog">
                    <div className="modal-dialog modal-lg" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">New Question</h5>
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close" onClick={toggleModal}>
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div className="modal-body">
                                <form onSubmit={handleSubmit}>
                                    <div className="form-group">
                                        <label htmlFor="title">Title</label>
                                        <input type="text" className="form-control" id="title" value={title} onChange={(e) => setTitle(e.target.value)} required />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="content">Content</label>
                                        <textarea className="form-control" id="content" value={content} onChange={(e) => setContent(e.target.value)} required />
                                    </div>
                                    <button type="submit" className="btn btn-primary">Post</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}

export default NewDiscussionModal;
