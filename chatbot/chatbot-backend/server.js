const express = require('express');
const mongoose = require('mongoose');
const openai = require('openai').default; 
const mockReply = require('./mockReplies');


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
    createdAt: { type: Date, default: Date.now }, 
    comments: [{
      user: String,
      avatarUrl: String,
      content: String,
      replyTime: String,
      views: Number
    }]
  });
  
const Discussion = mongoose.model('Discussion', discussionSchema);
  
  // Function to generate a response to a question using OpenAI
async function generateResponse(question) {
    try {
        // Initialize the OpenAI API instance with your API key
        const apiKey = process.env.OPENAI_API_KEY; // Load your API key from environment variable
        const openaiInstance = new openai(apiKey);

        // Make an API request to generate a response
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
        //const response = await openaiInstance.completions.create({
            model: 'gpt-4',
            messages: [ // Change the prompt parameter to messages parameter
              {'role': 'user', 'content': 'Hello!'}
            ],
            temperature: 0   
        });
        // Extract the last message from the response as it contains the model's response
        //const lastMessage = response.data.messages[response.data.messages.length - 1];
        //return response.data.choices[0].text.trim();
        
        // Return the generated response
        return response.choices[0].message.content;
    } catch (error) {
        console.error('Error generating response:', error);
        return "I'm sorry, I encountered an error while generating a response.";
    }
}
  
  
  // API Routes
app.get('/api/discussions', async (req, res) => {
    try {
        const discussions = await Discussion.find().sort({ createdAt: -1 }); // Sorting by creation time
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

  app.get('/api/discussions/:id', async (req, res) => {
    try {
        const discussion = await Discussion.findById(req.params.id);
        if (!discussion) {
            return res.status(404).json({ message: 'Discussion not found' });
        }
        res.json({
            id: discussion._id.toString(),
            ...discussion.toObject()
        });
    } catch (error) {
        console.error('Failed to fetch discussion:', error);
        res.status(500).json({ message: 'Failed to fetch discussion' });
    }
});


  app.post('/api/discussions', async (req, res) => {
    const { question } = req.body; // Extract question from request body
    // Generate response from OpenAI
    try {
      const response = await generateResponse(question);
    
      const newDiscussion = new Discussion({
        ...req.body,
        comments: [{
        user: 'ETA',
        avatarUrl: 'http://localhost:3000/ETA.png', // Adjust the URL if needed
        content: response, //mockReply,
        replyTime: new Date().toLocaleString(), // Example to generate a "Just now" time string
        views: 1
      }]
    });
      const savedDiscussion = await newDiscussion.save();
      res.json(savedDiscussion);
    } catch (error) {
      console.error('Failed to save new discussion:', error);
      res.status(500).send(error);
    }
  });
  
  // New endpoint for handling chat interactions with OpenAI
  app.post('/api/chat', async (req, res) => {
    const { question } = req.body;

    try {
        const response = await generateResponse(question);
        res.json({ response });
    } catch (error) {
        console.error('Error generating chat response:', error);
        res.status(500).json({ message: 'Failed to generate chat response' });
    }
});

  
  // Start the server
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
