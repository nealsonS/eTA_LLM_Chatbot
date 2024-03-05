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
  db.query('SELECT * FROM well_data WHERE longitude <> "Unknown" AND latitude <> "Unknown"', (error, results) => {
    if (error) {
      console.error('Error fetching data:', error); // Log any errors
      res.status(500).send('Error fetching data'); // Send an error response
      return;
    }
    
    // Transform the results into the desired format
    const transformedResults = results.map(entry => ({
      address: entry.address,
      well_name: entry.well_name,
      well_status: entry.well_status,
      well_type: entry.well_type,
      closest_city: entry.closest_city,
      barrels_of_oil: entry.barrels_of_oil,
      barrels_of_gas: entry.barrels_of_gas,
      position: {
        lat: parseFloat(entry.latitude), // Ensure latitude is a float
        lng: parseFloat(entry.longitude), // Ensure longitude is a float
      },
    }));

    // Send the transformed results as JSON
    res.json(transformedResults);
    console.log('Fetched data:', transformedResults);
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
