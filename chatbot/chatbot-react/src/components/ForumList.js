// src/components/ForumList.js
import React from 'react';
import ForumItem from './ForumItem';
import ForumControls from './ForumControls'; // Import the new component


// Example data array for forum discussions
const discussions = [
  {
    id: 1,
    title: 'Realtime fetching data',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'drewdan',
    replyTime: '13 minutes ago',
    views: 19,
    comments: 3,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar1.png',
  },
  {
    id: 2,
    title: 'Laravel 7 database backup',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'jlrdw',
    replyTime: '3 hours ago',
    views: 18,
    comments: 1,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
  },
  // ...more discussion objects
];

function ForumList() {
    return (
      <div className="inner-main">
        <ForumControls /> {/* Use the ForumControls component */}
        <div>
          {discussions.map((discussion) => (
            <ForumItem key={discussion.id} data={discussion} />
          ))}
        </div>
      </div>
    );
  }

export default ForumList;
