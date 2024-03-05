const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors()); // Use CORS to allow requests from your frontend

const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'lab5'
});

app.get('/api/wells', (req, res) => {
  db.query('SELECT * FROM well_data', (error, results) => {
    if (error) throw error;
    res.json(results);
    console.log(results);
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
