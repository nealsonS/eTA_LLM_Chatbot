// src/components/DiscussionDetail.js
import React from 'react';
import { useParams } from 'react-router-dom';
import { discussions } from './ForumList';  // Make sure discussions are exported from ForumList

function DiscussionDetail() {
  const { id } = useParams();
  const discussion = discussions.find(d => d.id === parseInt(id));

  if (!discussion) {
    return <div className="alert alert-danger" role="alert">
      Discussion not found!
    </div>;
  }

  return (
    <div className="container mt-5">
      <div className="inner-main-body p-2 p-sm-3 collapse forum-content show">
        <div className="card mb-2">
          <div className="card-body">
            <div className="media forum-item">
              <img src={discussion.avatarUrl} className="mr-3 rounded-circle" width="50" alt="User" />
              <div className="media-body">
                <h5 className="mt-1">{discussion.title}</h5>
                <p className="text-muted">{discussion.content}</p>
                <div className="text-muted small">
                  <span>{discussion.user}, {discussion.replyTime}</span>
                </div>
                <div className="text-muted small text-center align-self-center">
                  <span><i className="far fa-eye"></i> {discussion.views}</span>
                  <span><i className="far fa-comment ml-2"></i> {discussion.comments}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="card mb-2">
          {/* Additional content or replies could be placed here */}
        </div>
      </div>
    </div>
  );
}

export default DiscussionDetail;
