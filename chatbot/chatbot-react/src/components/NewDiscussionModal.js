import React, { useState } from 'react';

function NewDiscussionModal() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => setIsOpen(!isOpen);

  return (
    <>
      {/* Center the button using Bootstrap grid system */}
      <div className="modal-trigger-wrapper border-bottom">
        <div className="d-flex justify-content-center bg-white p-2">
            <button className="btn btn-primary btn-block font-weight-bold" onClick={toggleModal}>+ New Discussion</button>
        </div>
      </div>
      {isOpen && (
        <>
          <div className="modal fade show" style={{ display: 'block' }} tabIndex="-1" role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              <div className="modal-content">
                <div className="modal-header d-flex align-items-center bg-primary text-white">
                  <h6 className="modal-title mb-0" id="threadModalLabel">New Discussion</h6>
                  <button type="button" className="close" data-dismiss="modal" aria-label="Close" onClick={toggleModal}>
                    <span aria-hidden="true">×</span>
                  </button>
                </div>
                <div className="modal-body text-left">
                  <div className="form-group">
                    <label htmlFor="threadTitle">Title</label>
                    <input type="text" className="form-control" id="threadTitle" placeholder="Enter title" autoFocus />
                  </div>
        
                  <div className="custom-file form-control-sm mt-3">
                    <input type="file" className="custom-file-input" id="customFile" multiple />
                    <label className="custom-file-label" for="customFile">Choose files</label>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={toggleModal}>Cancel</button>
                  <button type="button" className="btn btn-primary">Post</button>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show"></div>
        </>
      )}
    </>
  );
}

export default NewDiscussionModal;
