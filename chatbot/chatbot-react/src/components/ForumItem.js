import React from 'react';
import { Link } from 'react-router-dom';

function ForumItem({ data }) {
    // Function to limit the content to the first two lines or 100 characters
    const formatContentPreview = (content) => {
        return content.length > 100 ? content.substring(0, 100) + "..." : content;
    };

    return (
        <div className="card mb-2" style={{ backgroundColor: 'whitesmoke' }}>
          <div className="card-body p-2">
            <div className="row align-items-center">
              <div className="col-2 text-center">
                <img src={data.avatarUrl} className="rounded-circle" width="50" alt="User" />
              </div>
              <div className="col-8">
                <h6 className="mb-1">
                  <Link to={`/discussion/${data._id}`} className="text-dark">{data.title}</Link>
                </h6>
                <p className="text-muted small mb-0">{formatContentPreview(data.content)}</p>
              </div>
              <div className="col-2 text-center">
                <small className="text-muted">{data.replyTime}</small>
              </div>
            </div>
          </div>
        </div>
    );
}

export default ForumItem;
