// src/components/DiscussionDetail.js
import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { discussions } from '../mockData';  // Ensure discussions are exported

function DiscussionDetail() {
  const { id } = useParams();
  const discussion = discussions.find(d => d.id === parseInt(id));

  if (!discussion) {
    return <div className="alert alert-danger">Discussion not found!</div>;
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
                <a href="javascript:void(0)" className="text-secondary">{discussion.user}</a> replied <span className="font-weight-bold">{discussion.replyTime}</span>
              </div>
              {discussion.comments.map((comment, index) => (
                <div className="media mt-3 forum-item" key={index}>
                  <img src={comment.avatarUrl} className="mr-3 rounded-circle" alt="Replier" width="50" />
                  <div className="media-body">
                    <h6 className="mt-1">{comment.user}</h6>
                    <p>{comment.content}</p>
                    <div className="text-muted">
                      <small className="text-muted ml-2">{comment.replyTime}</small>
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
