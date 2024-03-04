import mysql from 'mysql';
import util from 'util';

const dbConfig = {
    host: 'localhost',
    user: 'root',
    //password: '',
    database: 'demo1'
};

const connection = mysql.createConnection(dbConfig);
const query = util.promisify(connection.query).bind(connection);

const fetchDataFromDB = async () => {
    let well_info = [];
    try {
        await connection.connect();
        const query2 = "SELECT longitude, latitude FROM well_data WHERE longitude != 'Unknown' and latitude != 'Unknown'";
        const results = await query(query2);

        results.forEach(row => {
            well_info.push(row.longitude, row.latitude);
        });

        //console.log("results from promises", results);
        //console.log("well_info from promises", well_info);
        return well_info;

    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        await connection.end();
    }
};

export default { fetchDataFromDB };
