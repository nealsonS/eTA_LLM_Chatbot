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

mongoose.connection.once('open', function() {
  console.log("Successfully connected to MongoDB.");
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
  comments: Number
});

const Discussion = mongoose.model('Discussion', discussionSchema);

// API Routes
app.get('/api/discussions', async (req, res) => {
  const discussions = await Discussion.find();
  res.json(discussions);
});

app.post('/api/discussions', async (req, res) => {
  const newDiscussion = new Discussion(req.body);
  const savedDiscussion = await newDiscussion.save();
  res.json(savedDiscussion);
});

// Start the server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
