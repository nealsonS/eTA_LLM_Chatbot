// src/mockData.js

export const discussions = [
    {
        id: 1,
        title: 'Realtime fetching data',
        content: 'Hellooo :) I\'m newbie with Laravel and I want to fetch data from the database in realtime for my dashboard analytics. I found a solution with Ajax but it doesn\'t work. If anyone has a simple solution, it would be very helpful. Thank you!',
        user: 'Mokrani',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar1.png',
        replyTime: '1 hour ago',
        views: 19,
        comments: [
            {
                user: 'drewdan',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
                content: 'What exactly doesn\'t work with your Ajax calls? Have you checked the network tab in your developer tools to see the request?',
                replyTime: '45 minutes ago',
                views: 5
            }
        ]
    },
    {
        id: 2,
        title: 'Laravel 7 database backup',
        content: 'Can anyone recommend a reliable way to back up a Laravel application\'s database periodically? What tools or plugins do you use?',
        user: 'jlrdw',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
        replyTime: '3 hours ago',
        views: 18,
        comments: [
            {
                user: 'ciungulete',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
                content: 'Have you tried using Laravel\'s built-in backup solutions like spatie/laravel-backup package? It is quite comprehensive.',
                replyTime: '2 hours ago',
                views: 8
            }
        ]
    },
    {
        id: 3,
        title: 'Http client post raw content',
        content: 'I\'m trying to send JSON data to a server endpoint using the HTTP client in Node.js but keep getting errors about headers. Has anyone faced this before?',
        user: 'ciungulete',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
        replyTime: '7 hours ago',
        views: 32,
        comments: [
            {
                user: 'TechGuru',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
                content: 'Check your headers for content type. It sounds like your content type might not be set correctly for JSON.',
                replyTime: '6 hours ago',
                views: 10
            },
            {
                user: 'NodeNovice',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar5.png',
                content: 'This could also be a CORS issue. Make sure your server accepts requests from your client\'s domain.',
                replyTime: '5 hours ago',
                views: 8
            }
        ]
    },
    {
        id: 4,
        title: 'Top rated filter not working',
        content: 'I\'ve implemented a top-rated filter for products in my eCommerce site using Django, but it doesn\'t seem to sort them correctly. Any tips?',
        user: 'bugsysha',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
        replyTime: '11 hours ago',
        views: 49,
        comments: [
            {
                user: 'DjangoDude',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar6.png',
                content: 'Are you using Django\'s ORM ordering? It might be worthwhile to check your querysets.',
                replyTime: '10 hours ago',
                views: 15
            }
        ]
    },
    {
        id: 5,
        title: 'Create a delimiter field',
        content: 'I need to store multiple values in a single database field. Should I use delimited strings, JSON, or is there another option I\'m missing?',
        user: 'jackalds',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar5.png',
        replyTime: '12 hours ago',
        views: 65,
        comments: [
            {
                user: 'DataWizard',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar7.png',
                content: 'JSON would be more flexible and searchable compared to delimited strings, especially if your database supports JSON types.',
                replyTime: '11 hours ago',
                views: 20
            }
        ]
    },
    {
        id: 6,
        title: 'One model 4 tables',
        content: 'Is it possible to use one model to interact with different tables depending on the business logic? How can I implement this in Laravel?',
        user: 'bugsysha',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar6.png',
        replyTime: '14 hours ago',
        views: 45,
        comments: [
            {
                user: 'LaraGuru',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar1.png',
                content: 'Laravel doesn\'t directly support this but you can dynamically change the table associated with a model using the setTable method.',
                replyTime: '13 hours ago',
                views: 12
            }
        ]
    },
    {
        id: 7,
        title: 'Auth attempt returns false',
        content: 'Every time I try to authenticate using Laravel\'s built-in Auth, I get false, even with correct credentials. Where should I start debugging?',
        user: 'michaeloravec',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar7.png',
        replyTime: '18 hours ago',
        views: 70,
        comments: [
            {
                user: 'AuthMaster',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar2.png',
                content: 'First, check your user provider configurations in your auth.php config file. It\'s common to have issues there if not set up correctly.',
                replyTime: '17 hours ago',
                views: 22
            }
        ]
    },
    {
        id: 8,
        title: 'Create a delimiter field',
        content: 'I need to store multiple values in a single database field. Should I use delimited strings, JSON, or is there another option I\'m missing?',
        user: 'jackalds',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar5.png',
        replyTime: '12 hours ago',
        views: 65,
        comments: [
            {
                user: 'DataWizard',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar7.png',
                content: 'JSON would be more flexible and searchable compared to delimited strings, especially if your database supports JSON types.',
                replyTime: '11 hours ago',
                views: 20
            }
        ]
    },
    {
        id: 9,
        title: 'Http client post raw content',
        content: 'I\'m trying to send JSON data to a server endpoint using the HTTP client in Node.js but keep getting errors about headers. Has anyone faced this before?',
        user: 'ciungulete',
        avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar4.png',
        replyTime: '7 hours ago',
        views: 32,
        comments: [
            {
                user: 'TechGuru',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar3.png',
                content: 'Check your headers for content type. It sounds like your content type might not be set correctly for JSON.',
                replyTime: '6 hours ago',
                views: 10
            },
            {
                user: 'NodeNovice',
                avatarUrl: 'https://bootdey.com/img/Content/avatar/avatar5.png',
                content: 'This could also be a CORS issue. Make sure your server accepts requests from your client\'s domain.',
                replyTime: '5 hours ago',
                views: 8
            }
        ]
    },
  ];