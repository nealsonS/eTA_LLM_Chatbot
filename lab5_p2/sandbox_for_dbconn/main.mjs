import pkg from './promises.mjs'; //connect to MySQL
import { Point } from 'ol/geom.js'; 
import { Feature, Map, Overlay, View } from 'ol/index.js';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer.js';
import { OSM, Vector as VectorSource } from 'ol/source.js';
import { useGeographic } from 'ol/proj.js';


const { fetchDataFromDB } = pkg;

const fetchData = async () => {
    var well_info = await fetchDataFromDB();
    //console.log("well_info in promises.mjs:", well_info);
    return well_info;
};

const main = async () => { // write all the code in this function
    // Assuming fetchData returns an array of places
    var places = await fetchData();
    console.log("places:", places);

    // debugging 
    //places.forEach((place, index) => {
    //    console.log(`Index ${index}:`);
    //    console.log("well_name:", place.well_name);
    //    console.log("address:", place.address);
    //    console.log("well_status:", place.well_status);
    //    console.log("well_type:", place.well_type);
    //    console.log("closest_city:", place.closest_city);
    //    console.log("barrels_of_oil:", place.barrels_of_oil);
    //    console.log("barrels_of_gas:", place.barrels_of_gas);
    //});

    // create features from places, use for window of information for each point
    const features = places.map((place, index) => {
        // Assuming Point and Feature are classes provided by your mapping library
        const point = new Point(place.longitude, place.latitude);
        const feature = new Feature(point);
        feature.setProperties({
            well_name: place.well_name,
            address: place.address,
            well_status: place.well_status,
            well_type: place.well_type,
            closest_city: place.closest_city,
            barrels_of_oil: place.barrels_of_oil,
            barrels_of_gas: place.barrels_of_gas,
        });

        //console.log("feature", feature);
        return feature;
    });

    const map = new Map({
      target: 'map',
      view: new View({
        center: places[0],  // initial point
        zoom: 13, // set zoom look out and see many points
      }),
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
        new VectorLayer({
          source: new VectorSource({
            features: features,
          }),
          style: {
            'circle-radius': 9,
            'circle-fill-color': 'red',
          },
        }),
      ],
    });
    
    
    
    
    
};


main();
