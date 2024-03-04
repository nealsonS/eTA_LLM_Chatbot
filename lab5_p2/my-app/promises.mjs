// promises.mjs
//import { fetchDataFromDB } from './promises.js';

import pkg from './promises.js';
const { fetchDataFromDB } = pkg;


const fetchData = async () => {
    const well_info = await fetchDataFromDB();
    console.log("Imported Well Info:", well_info);

    // ... rest of your code
};

fetchData();

