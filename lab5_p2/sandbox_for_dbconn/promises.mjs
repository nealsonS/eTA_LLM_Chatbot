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
        const query1 = "SELECT longitude, latitude, well_name, address, well_status, well_type, closest_city, barrels_of_oil, barrels_of_gas FROM well_data WHERE longitude != 'Unknown' and latitude != 'Unknown'";
        const results = await query(query1);

        results.forEach(row => {
            well_info.push({"longitude": row.longitude, "latitude": row.latitude, "well_name": row.well_name, "address": row.address, "well_status": row.well_status, "well_type": row.well_type, "closest_city": row.closest_city, "barrels_of_oil": row.barrels_of_oil, "barrels_of_gas": row.barrels_of_gas});
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
