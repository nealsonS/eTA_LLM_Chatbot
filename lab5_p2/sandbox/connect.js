//import { fetchDataFromDB } from './promises.js'; //get commonJS error
import pkg from './promises.js';
const { fetchDataFromDB } = pkg;

const fetchData = async () => {
    const well_info = await fetchDataFromDB();
    console.log("well_info in connect.js:", well_info);
};

fetchData();

