function add(a, b) {
    return a + b;
}

function coordinates(latitude, longitude) {
    var coor = [];
    for (var i = 0; i < latitude.length; i++) {
        if (latitude[i] !== "Unknown" && longitude[i] !== "Unknown") {
            coor.push([parseFloat(longitude[i]), parseFloat(latitude[i])]);
        }
    }
    return coor;
}

function get_info(well_name, latitude, longitude, address, well_status, well_type, closest_city, barrels_of_oil, barrels_of_gas) {
    var coor = [];
    for (var i = 0; i < latitude.length; i++) {
        if (latitude[i] !== "Unknown" && longitude[i] !== "Unknown") {
            coor.push([well_name, parseFloat(longitude[i]), parseFloat(latitude[i]), address, well_status, well_type, closest_city, barrels_of_oil, barrels_of_gas]);
        }
    }
    return coor;
}

