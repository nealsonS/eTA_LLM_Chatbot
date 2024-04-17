// src/components/ForumList.js
import React from 'react';
import ForumItem from './ForumItem';  // This will display each item in the list
import ForumControls from './ForumControls';  // Controls like filters or search, assuming it's defined

export const discussions = [
  {
    id: 1,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar1.png',
    user: 'Mokrani',
    title: 'Realtime fetching data',
    content: "Hellooo :) I'm newbie with Laravel and I want to fetch data from database in realtime for my dashboard analytics. I found a solution with AJAX but it doesn't work. If anyone has a simple solution, it would be helpful.",
    replyTime: '1 hour ago',
    views: 189,
    comments: [
      {
        user: 'drewdan',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
        content: "What exactly doesn't work with your AJAX calls? Also, WebSockets are a great solution for realtime data on a dashboard. Laravel offers this out of the box using broadcasting.",
        replyTime: '45 minutes ago',
        views: 102,
      }
    ],
  },
  {
    id: 2,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
    user: 'jlrdw',
    title: 'Laravel 7 database backup',
    content: 'I am struggling to set up my database backups in Laravel 7. Does anyone have a robust solution or a preferred package?',
    replyTime: '2 hours ago',
    views: 78,
    comments: [
      {
        user: 'ciungulete',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
        content: "Have you tried Spatie's Laravel Backup package? It's very comprehensive and easy to set up.",
        replyTime: '1 hour ago',
        views: 56,
      }
    ],
  },
  // Add more discussions following the same format...
  {
    id: 3,
    avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
    user: 'ciungulete',
    title: 'HTTP client post raw content',
    content: "I'm trying to post raw JSON data using HTTP client in PHP but keep getting errors. Any tips?",
    replyTime: '3 hours ago',
    views: 45,
    comments: [
      {
        user: 'bugsysha',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
        content: "Ensure your headers are set correctly to 'Content-Type: application/json'. That might solve your issue.",
        replyTime: '2 hours ago',
        views: 33,
      }
    ],
  },
  // Repeat for ids 4, 5, 6, 7 with different content...
];

function ForumList() {
  return (
    <div className="inner-main">
      <ForumControls />
      {discussions.map(discussion => (
        <ForumItem key={discussion.id} data={discussion} />
      ))}
    </div>
  );
}

export default ForumList;
