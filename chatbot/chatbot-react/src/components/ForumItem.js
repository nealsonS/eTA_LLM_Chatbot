// src/components/ForumItem.js
import React from 'react';

function ForumItem({ data }) {
  return (
    <div className="card mb-2 forum-item">
      <div className="card-body p-2 p-sm-3">
        <div className="media">
          <img src={data.avatarUrl} className="mr-3 rounded-circle" width="50" alt="User" />
          <div className="media-body">
            <h6 className="title">{data.title}</h6>
            <p className="content">{data.content}</p>
            <p className="user-info">
              <a href={`user/${data.user}`}>{data.user}</a> replied <span>{data.replyTime}</span>
            </p>
          </div>
          <div className="text-muted small text-center align-self-center">
            <span><i className="far fa-eye"></i> {data.views}</span>
            <span><i className="far fa-comment ml-2"></i> {data.comments}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ForumItem;
