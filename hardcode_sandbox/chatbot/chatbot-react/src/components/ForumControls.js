// src/components/ForumControls.js
import React from 'react';

function ForumControls() {
    return (
        <div className="modal-trigger-wrapper border-bottom pb-2">
            <div className="inner-main-header d-flex justify-content-between align-items-center bg-white p-3 mt-3">
                <div>
                    <select className="custom-select custom-select-sm mr-1">
                        <option selected>Latest</option>
                        <option value="1">Popular</option>
                        <option value="2">Solved</option>
                        <option value="3">Unsolved</option>
                        <option value="4">No Replies Yet</option>
                    </select>
                </div>
                <span>
                    <input type="text" className="form-control form-control-sm bg-gray-200 border-gray-200 shadow-none" placeholder="Search forum" />
                </span>
            </div>
        </div>
    );
}

export default ForumControls;
