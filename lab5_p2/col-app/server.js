const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors()); // Use CORS to allow requests from your frontend

// Create a connection to the database
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'lab5'
});

// Endpoint to fetch well data
app.get('/api/wells', (req, res) => {
  // Query to select all records from the 'well_data' table
  db.query('SELECT * FROM well_data', (error, results) => {
    if (error) {
      console.error('Error fetching data:', error); // Log any errors
      res.status(500).send('Error fetching data'); // Send an error response
      return;
    }
    // Send the results as JSON
    res.json(results);
    // Log the fetched data to the terminal
    console.log('Fetched data:', results);
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
