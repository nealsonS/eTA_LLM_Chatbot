
import mysql from 'mysql2/promise';

const dbConfig = {
    host: 'localhost',
    user: 'root',
    //password: '',
    database: 'demo1'
};

// Removed util.promisify since mysql2/promise already supports promises
const fetchDataFromDB = async () => {
    let well_info = [];
    try {
        const connection = await mysql.createConnection(dbConfig);
        console.log('Successfully connected to the MySQL server.'); // Log connection success
        
        const query2 = "SELECT longitude, latitude FROM well_data WHERE longitude != 'Unknown' and latitude != 'Unknown'";
        const [results] = await connection.query(query2);

        results.forEach(row => {
            well_info.push({longitude: row.longitude, latitude: row.latitude});
        });

        console.log("Results from SQL database:", well_info); // Log fetched data
        return well_info;

    } catch (error) {
        console.error('Error fetching data from MySQL:', error);
    } finally {
        if (connection) await connection.end();
    }
};

export default { fetchDataFromDB };

