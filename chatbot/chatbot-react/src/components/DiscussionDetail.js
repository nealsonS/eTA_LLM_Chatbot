// src/components/DiscussionDetail.js
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { formatDate } from '../formatDate'; // Import the utility function
import examplePdf from '../textbook.pdf';


function DiscussionDetail({ user }) {
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

    const intervalId = setInterval(fetchDiscussion, 1000);  // Poll every 1 seconds
    return () => clearInterval(intervalId);  // Clean up the interval on component unmount
  }, [id]);  // Re-run this effect if the ID changes

  const handleVerify = async () => {
    // Make API call to verify the discussion
    const response = await fetch(`http://localhost:3800/api/discussions/verify/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ isVerified: true })
    });
    if (response.ok) {
      setDiscussion({ ...discussion, isVerified: true });
    }
  };


  if (!discussion) {
    return <div class="d-flex justify-content-center">
              <div class="spinner-border" role="status">
                <span class="sr-only">Loading...</span>
              </div>
            </div>;
  }
  console.log({user})

  return (
    <div className="container mt-5" >
      <Link to="/" className="btn btn-light btn-sm mb-3 has-icon">
        <i className="fa fa-arrow-left mr-2"></i>Back
      </Link>
      <div className="card mb-2" style={{ backgroundColor: 'whitesmoke' }}>
        <div className="card-body">
          <div className="media forum-item">
            <img src={discussion.avatarUrl} className="mr-3 rounded-circle" alt="User" width="50" />
            <div className="media-body">
              <h5 className="mt-1">{discussion.title}</h5>
              <p>{discussion.content}</p>
              <div className="text-muted">
                <a href="javascript:void(0)" className="text-secondary">{formatDate(discussion.createdAt)}</a> 
              </div>
              <div>
                {discussion.comments.map((comment, index) => (
                  <div className="media mt-3 forum-item" key={index}>
                    <img src={comment.avatarUrl} className="mr-3 rounded-circle" alt="Replier" width="50" />
                    <div className="media-body">
                      <h6 className="mt-1">{comment.user}</h6>
                      {comment.content.length > 0 ? (
                      <div>
                        <p>{comment.content}</p>
                        <div>
                          {comment.Booksrc.length > 0 && (
                          <iframe
                            src={`${examplePdf}#page=${comment.pageno}`}
                            width="100%"
                            height="500px"
                            allow="fullscreen;"
                          >
                          <p>Your browser does not support PDFs. <a href="/path/to/document.pdf">Download the PDF</a>.</p>
                          </iframe>
                          )}

                        </div>
                        <div className="mt-4">
                          {comment.YTEmbedLink.length > 0 && (
                            <iframe
                              width="100%"
                              height="500px"
                              src={`https://www.youtube.com/embed/${comment.YTEmbedLink}?start=${comment.YT_time}`}
                              title="YouTube video player"
                              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                              referrerPolicy="strict-origin-when-cross-origin"
                              allowFullScreen
                            ></iframe>
                          )}
                        </div>
                        <div className="text-muted">
                          <small className="text-muted ml-2">{formatDate(comment.replyTime)}</small>
                        </div>
                      </div>
                      ): (
                      <div className="spinner-grow" style={{width: 20, height: 20}} role="status">
                        <span className="sr-only">Loading...</span>
                      </div>
                      )}
                      
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className='m-3'>
            <p className={discussion.isVerified ? "text-success" : "text-danger"}>
              {discussion.isVerified ? 
                <div>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                  </svg>
                  {" "}This response is verified by TA
                </div> 
              : <div>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4m.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>
                  </svg>
                  {" "}This response is not yet verified by TA
                </div>}
            </p>
            {user && user.isTA && !discussion.isVerified && (
              <div className="col-3">
                <button className="btn btn-primary btn-sm btn-block" onClick={handleVerify}>Verify</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DiscussionDetail;
