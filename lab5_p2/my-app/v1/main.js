import { Feature, Map, Overlay, View } from 'ol/index.js';
import { OSM, Vector as VectorSource } from 'ol/source.js';
import { Point } from 'ol/geom.js';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer.js';
import { useGeographic } from 'ol/proj.js';

useGeographic();

const places = [
  [-103.73, 48.11],
  [-103.7329, 48.1094],
  [103.602608, 48.03581],
  [-103.728, 48.109],
  [-103.728, 48.109],
  [103.35, 48.02],
  [-103.73, 48.11],
  [-103.7312, 48.1094],
];

const wellData = [
  { well_name: 'a', address: 'a', well_status: 'a', well_type: 'a', closest_city: 'a', barrels_of_oil: 'a', barrels_of_gas: 'a' },
  { well_name: 'b', address: 'b', well_status: 'b', well_type: 'b', closest_city: 'b', barrels_of_oil: 'b', barrels_of_gas: 'b' },
  { well_name: 'c', address: 'c', well_status: 'c', well_type: 'c', closest_city: 'c', barrels_of_oil: 'c', barrels_of_gas: 'c' },
  { well_name: 'd', address: 'd', well_status: 'd', well_type: 'd', closest_city: 'd', barrels_of_oil: 'd', barrels_of_gas: 'd' },
  { well_name: 'e', address: 'e', well_status: 'e', well_type: 'e', closest_city: 'e', barrels_of_oil: 'e', barrels_of_gas: 'e' },
  { well_name: 'f', address: 'f', well_status: 'f', well_type: 'f', closest_city: 'f', barrels_of_oil: 'f', barrels_of_gas: 'f' },
  { well_name: 'g', address: 'g', well_status: 'g', well_type: 'g', closest_city: 'g', barrels_of_oil: 'g', barrels_of_gas: 'g' },
  { well_name: 'h', address: 'h', well_status: 'h', well_type: 'h', closest_city: 'h', barrels_of_oil: 'h', barrels_of_gas: 'h' },
];

const features = wellData.map((data, index) => {
  const place = places[index];
  const point = new Point(place);
  const feature = new Feature(point);
  feature.setProperties(data);
  console.log("feature", feature);
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


const element = document.getElementById('popup');

const popup = new Overlay({
  element: element,
  stopEvent: false,
});
map.addOverlay(popup);

const info = document.getElementById('info');

map.on('moveend', function () {
  const view = map.getView();
  const center = view.getCenter();
  //info.innerHTML = formatCoordinate(center);
  updateInfo(center); // Update the info panel with the center coordinates
});

let popover;

map.on('click', function (event) {
  if (popover) {
    popover.dispose();
    popover = undefined;
  }
  const feature = map.getFeaturesAtPixel(event.pixel)[0];
  if (!feature) {
    return;
  }
  
  // Get additional properties of the feature
  const wellName = feature.get('well_name');
  const address = feature.get('address');
  const wellStatus = feature.get('well_status');
  const wellType = feature.get('well_type');
  const closestCity = feature.get('closest_city');
  const barrels_of_oil = feature.get('barrels_of_oil');
  const barrels_of_gas = feature.get('barrels_of_gas');
  
  
  const coordinate = feature.getGeometry().getCoordinates();
  popup.setPosition([
    coordinate[0] + Math.round(event.coordinate[0] / 360) * 360,
    coordinate[1],
  ]);

  console.log("coordinate", coordinate);
  console.log("wellName", wellName);
  console.log("address", address);
  console.log("wellStatus", wellStatus);
  console.log("wellType", wellType);
  console.log("closestCity", closestCity);
  console.log("barrels_of_oil", barrels_of_oil);
  console.log("barrels_of_gas", barrels_of_gas);
  
  popover = new bootstrap.Popover(element, {
    container: element.parentElement,
    content: formatCoordinate(wellName, coordinate, address, wellStatus, wellType, closestCity, barrels_of_oil, barrels_of_gas),
    html: true,
    offset: [0, 20],
    placement: 'top',
    sanitize: false,
  });
  popover.show();
});

map.on('pointermove', function (event) {
  const type = map.hasFeatureAtPixel(event.pixel) ? 'pointer' : 'inherit';
  map.getViewport().style.cursor = type;
});



function updateInfo(coordinate, wellName = "NA", address = "NA", wellStatus = "NA", wellType = "NA", closestCity = "NA", barrels_of_oil = "NA", barrels_of_gas = "NA") {
  const centerCoordinate = map.getView().getCenter();
  info.innerHTML = formatCoordinate(wellName, centerCoordinate, address, wellStatus, wellType, closestCity, barrels_of_oil, barrels_of_gas);
}


function formatCoordinate(wellName, coordinate, address, wellStatus, wellType, closestCity, barrels_of_oil, barrels_of_gas) {
  return `
    <table>
      <tbody> 
        <tr><th>well name</th><td>${wellName}NA</td></tr>
        <tr><th>longitude</th><td>${coordinate[0].toFixed(2)}</td></tr>
        <tr><th>latitude</th><td>${coordinate[1].toFixed(2)}</td></tr>
        <tr><th>address</th><td>${address}</td></tr>
        <tr><th>well status</th><td>${wellStatus}</td></tr>
        <tr><th>well type</th><td>${wellType}</td></tr>
        <tr><th>closest city</th><td>${closestCity}</td></tr>
        <tr><th>barrel of oil</th><td>${barrels_of_oil}</td></tr>
        <tr><th>barrels of gas</th><td>${barrels_of_gas}</td></tr>
      </tbody>
    </table>`;
}

