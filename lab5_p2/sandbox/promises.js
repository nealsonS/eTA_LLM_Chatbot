const mysql = require('mysql');
const util = require('util');

// Create a MySQL connection
const dbConfig = {
    host: 'localhost',
    user: 'root',
    //password: 'your_password',
    database: 'demo1'
};

const connection = mysql.createConnection(dbConfig);

// Promisify the MySQL query function
const query = util.promisify(connection.query).bind(connection);

// Function to fetch data from a MySQL database using promises
const fetchDataFromDB = async () => {
    let well_info = [];
    try {
        // Establish a connection to the database
        await connection.connect();
	query2 = "SELECT longitude, latitude FROM well_data WHERE longitude != 'Unknown' and latitude != 'Unknown'"
        // Execute a query using the promisified query function
        const results = await query(query2);
	// Save each row into the list
        results.forEach(row => {
            well_info.push(row.longitude);
        });
        // Display the fetched data
        console.log(results);
        console.log("Longitude Data", well_info);

    } catch (error) {
        // Handle any errors that occurred during the process
        console.error('Error fetching data:', error);

    } finally {
        // Close the database connection
        await connection.end();
    }
};

// Call the async function to fetch data
fetchDataFromDB();

