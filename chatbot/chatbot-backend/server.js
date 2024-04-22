const express = require('express');
const mongoose = require('mongoose');

const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3800;

app.use(cors());
app.use(express.json()); // Middleware to parse JSON

const password = '770sGrandAve7058';
const MONGODB_URI = `mongodb+srv://ColinZWang:${password}@colinzwang-cluster.6civtdf.mongodb.net/?retryWrites=true&w=majority`;

console.log("Attempting to connect to MongoDB...");

mongoose.connect(MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  serverApi: {
    version: '1',
    strict: true,
    deprecationErrors: true
  }
});

const fetchAndLogDiscussions = async () => {
    try {
      const discussions = await Discussion.find(); // Fetch all discussions
      console.log("Example Discussion in the Database:");
      console.log(discussions[0]);
    } catch (error) {
      console.log("Error fetching discussions:", error);
    }
  };
  
  mongoose.connection.once('open', function() {
    console.log("Successfully connected to MongoDB.", "\n");
    fetchAndLogDiscussions(); // Fetch and log discussions once the database connection is open
  }).on('error', function(error) {
    console.log("Connection error:", error);
  });
  

// Define a schema and model for Forum Discussions
const discussionSchema = new mongoose.Schema({
    title: String,
    content: String,
    user: String,
    avatarUrl: String,
    replyTime: String,
    views: Number,
    comments: [{
      user: String,
      avatarUrl: String,
      content: String,
      replyTime: String,
      views: Number
    }]
  });
  
  const Discussion = mongoose.model('Discussion', discussionSchema);
  
  // API Routes
  app.get('/api/discussions', async (req, res) => {
    try {
      const discussions = await Discussion.find();
      res.json(discussions.map(discussion => ({
        id: discussion._id.toString(), // Convert ObjectId to string
        ...discussion.toObject(),
        comments: discussion.comments.map(comment => ({
          ...comment,
          id: comment._id.toString() // Convert ObjectId to string for each comment
        }))
      })));
    } catch (error) {
      console.error('Failed to fetch discussions:', error);
      res.status(500).json({ message: 'Failed to fetch discussions' });
    }
  });
  
  app.post('/api/discussions', async (req, res) => {
    const newDiscussion = new Discussion(req.body);
    try {
      const savedDiscussion = await newDiscussion.save();
      res.status(201).json(savedDiscussion);
    } catch (error) {
      console.error('Failed to save new discussion:', error);
      res.status(400).json({ message: 'Failed to add new discussion' });
    }
  });
  
  // Start the server
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));