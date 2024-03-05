//import { fetchDataFromDB } from './promises.js';
import pkg from './promises.mjs';
const { fetchDataFromDB } = pkg;

const fetchData = async () => {
    var well_info = await fetchDataFromDB();
    //console.log("well_info in promises.mjs:", well_info);
    return well_info;
};

const main = async () => { // write all the code in this function
    var places = await fetchData();
    console.log("places:", places);
    
     // Iterate over each place in the places array
    places.forEach((place, index) => {
        console.log(`Index ${index}:`);
        console.log("well_name:", place.well_name);
        console.log("address:", place.address);
        console.log("well_status:", place.well_status);
        console.log("well_type:", place.well_type);
        console.log("closest_city:", place.closest_city);
        console.log("barrels_of_oil:", place.barrels_of_oil);
        console.log("barrels_of_gas:", place.barrels_of_gas);
    });  
    
    
};


main();
