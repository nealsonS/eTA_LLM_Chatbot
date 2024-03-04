//import { fetchDataFromDB } from './promises.js';
import pkg from './promises.mjs';
const { fetchDataFromDB } = pkg;

const fetchData = async () => {
    const well_info = await fetchDataFromDB();
    console.log("well_info in promises.mjs:", well_info);
};

fetchData();

