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
  {
    id: 3,
    title: 'Http client post raw content',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'ciungulete',
    replyTime: '7 hours ago',
    views: 32,
    comments: 2,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
  },
  {
    id: 4,
    title: 'Top rated filter not working',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'bugsysha',
    replyTime: '11 hours ago',
    views: 49,
    comments: 9,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
  },
  {
    id: 5,
    title: 'Create a delimiter field',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'jackalds',
    replyTime: '12 hours ago',
    views: 65,
    comments: 10,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar5.png',
  },
  {
    id: 6,
    title: 'One model 4 tables',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'bugsysha',
    replyTime: '14 hours ago',
    views: 45,
    comments: 4,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar6.png',
  },
  {
    id: 7,
    title: 'Auth attempt returns false',
    content: 'lorem ipsum dolor sit amet lorem ipsum dolor sit amet lorem ipsum dolor sit amet',
    user: 'michaeloravec',
    replyTime: '18 hours ago',
    views: 70,
    comments: 3,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar7.png',
  }
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
