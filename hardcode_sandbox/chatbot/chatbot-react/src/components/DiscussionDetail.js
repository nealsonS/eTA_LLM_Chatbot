// src/components/DiscussionDetail.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { formatDate } from '../formatDate'; // Import the utility function


function DiscussionDetail() {
  const [discussion, setDiscussion] = useState(null);
  const { id } = useParams();  // Get the discussion ID from the URL
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDiscussion = async () => {
      try {
        const response = await fetch(`http://localhost:3800/api/discussions/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch');
      }
        const data = await response.json();
        setDiscussion(data);
      } catch (error) {
        console.error('Failed to fetch discussion:', error);
        setError('Failed to load discussion');
      }
    };

    fetchDiscussion();
  }, [id]);  // Re-run this effect if the ID changes

  

  if (!discussion) {
    return <div class="d-flex justify-content-center">
              <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
              </div>
            </div>;
  }

  return (
    <div className="container mt-5">
      <Link to="/" className="btn btn-light btn-sm mb-3 has-icon">
        <i className="fa fa-arrow-left mr-2"></i>Back
      </Link>
      <div className="card mb-2">
        <div className="card-body">
          <div className="media forum-item">
            <img src={discussion.avatarUrl} className="mr-3 rounded-circle" alt="User" width="50" />
            <div className="media-body">
              <h5 className="mt-1">{discussion.title}</h5>
              <p>{discussion.content}</p>
              <div className="text-muted">
                <a href="javascript:void(0)" className="text-secondary">{formatDate(discussion.createdAt)}</a> 
              </div>
              {discussion.comments.map((comment, index) => (
                <div className="media mt-3 forum-item" key={index}>
                  <img src={comment.avatarUrl} className="mr-3 rounded-circle" alt="Replier" width="50" />
                  <div className="media-body">
                    <h6 className="mt-1">{comment.user}</h6>
                    <p>{comment.content}</p>
                    <iframe width="560" 
                      height="315" 
                      src="https://www.youtube.com/embed/V5hhrDFo8Vk?si={discussion.YTEmbedLink}&amp;start=30" 
                      title="YouTube video player" 
                      frameborder="0" 
                      allow="accelerometer; 
                      autoplay; 
                      clipboard-write; 
                      encrypted-media; 
                      gyroscope; 
                      picture-in-picture; 
                      web-share" 
                      referrerpolicy="strict-origin-when-cross-origin" 
                      allowfullscreen>
                    </iframe>
                    <div className="text-muted">
                      <small className="text-muted ml-2">{formatDate(comment.replyTime)}</small>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DiscussionDetail;
