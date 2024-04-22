const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json()); // Middleware to parse JSON

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log("MongoDB connection established"))
.catch(err => console.error("Mongo connection error:", err));

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
