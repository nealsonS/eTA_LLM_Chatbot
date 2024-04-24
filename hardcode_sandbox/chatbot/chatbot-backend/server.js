const express = require('express');
const mongoose = require('mongoose');
const { spawn } = require('child_process');  // To spawn Python process
const cors = require('cors');

require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3800;

app.use(cors());
app.use(express.json()); // middleware to parse JSON

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
      const discussions = await Discussion.find(); // fetch all discussions
      console.log("Example Discussion in the Database:");
      console.log(discussions[0]);
    } catch (error) {
      console.log("Error fetching discussions:", error);
    }
  };
  
  mongoose.connection.once('open', function() {
    console.log("Successfully connected to MongoDB.", "\n");
    fetchAndLogDiscussions(); // fetch and log discussions once database connection is open
  }).on('error', function(error) {
    console.log("Connection error:", error);
  });
  

// define schema and model for Forum Discussions
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
  
  // generate response using OpenAI
async function generateResponse(question) {
    try {
        const apiKey = process.env.OPENAI_API_KEY; 
        const openaiInstance = new openai(apiKey);

        const response = await fetch('https://api.openai.com/v1/chat/completions', {
        //const response = await openaiInstance.completions.create({
            model: 'gpt-4',
            messages: [
              {'role': 'user', 'content': 'Hello!'}
            ],
            temperature: 0   
        });
        // Extract the last message from the response as it contains the model's response
        //const lastMessage = response.data.messages[response.data.messages.length - 1];
        //return response.data.choices[0].text.trim();
        
        return response.choices[0].message.content;
    } catch (error) {
        console.error('Error generating response:', error);
        return "I'm sorry, I encountered an error while generating a response.";
    }
}
  
  
// API routes
app.get('/api/discussions', async (req, res) => {
    try {
        const discussions = await Discussion.find().sort({ createdAt: -1 }); // sort by creation time
        res.json(discussions.map(discussion => ({
        id: discussion._id.toString(), // convert ObjectId to string
        ...discussion.toObject(),
        comments: discussion.comments.map(comment => ({
          ...comment,
          id: comment._id.toString() // convert ObjectId to string for each comment
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
// Function to execute Python script and get the AI response
function getAIResponse(userInput, callback) {
    const python = spawn('python3', ['../Milvus/chatbot.py', userInput]);
    let output = '';
  
    python.stdout.on('data', function (data) {
      output += data.toString();
    });
  
    python.on('close', (code) => {
      if (code !== 0) {
        return callback(new Error('Python script exited with code ' + code), null);
      }
      try {
        console.log(output)
        const parsedOutput = JSON.parse(output);
        callback(null, parsedOutput);
      } catch (parseError) {
        callback(new Error('Error parsing output: ' + parseError), null);
      }
    });
  }
  
  app.post('/api/discussions', async (req, res) => {
    const { title, content, user, avatarUrl } = req.body;
  
    getAIResponse(content, async (err, aiResponse) => {
      if (err) {
        console.error('Failed to get AI response:', err);
        return res.status(500).send('Failed to get AI response');
      }

      const embedURL = `https://www.youtube.com/embed/${aiResponse.vids}`
  
      try {
        const newDiscussion = new Discussion({
          title,
          content,
          user,
          avatarUrl,
          replyTime: new Date().toLocaleString(),
          views: 0,
          comments: [{
            user: 'ETA',
            avatarUrl: 'http://localhost:3000/ETA.png',
            content: aiResponse.response,
            YTEmbedLink: embedURL,
            replyTime: new Date().toLocaleString(),
            views: 0
          }]
        });
  
        const savedDiscussion = await newDiscussion.save();
        res.status(201).json(savedDiscussion);
      } catch (error) {
        console.error('Failed to save new discussion:', error);
        res.status(500).send(error.message);
      }
    });
  });

//   app.post('/api/discussions', async (req, res) => {
//     const newDiscussion = new Discussion({
//       ...req.body,
//       comments: [{
//         user: 'ETA',
//         avatarUrl: 'http://localhost:3000/ETA.png', // Adjust the URL if needed
//         content: mockReply,
//         replyTime: new Date().toLocaleString(), // Example to generate a "Just now" time string
//         views: 0
//       }]
//     });
//     try {
//       const savedDiscussion = await newDiscussion.save();
//       res.json(savedDiscussion);
//     } catch (error) {
//       console.error('Failed to save new discussion:', error);
//       res.status(500).send(error);
//     }
//   });
  
  
  // start server
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));