import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import {fromLonLat} from 'ol/proj';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';
import Overlay from 'ol/Overlay';

// Initialize the map
const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
  ],
  view: new View({
    center: fromLonLat([0, 0]), // Adjust as needed
    zoom: 2,
  }),
});

// Initialize vector source and layer for markers
const vectorSource = new VectorSource();
const vectorLayer = new VectorLayer({
  source: vectorSource,
  style: new Style({
    image: new CircleStyle({
      radius: 7,
      fill: new Fill({color: 'red'}),
      stroke: new Stroke({
        color: 'white',
        width: 2,
      }),
    }),
  }),
});

map.addLayer(vectorLayer);

// Create an overlay for popups
const overlayContainerElement = document.createElement('div');
overlayContainerElement.className = 'overlay-container';
const overlayContentElement = document.createElement('div');
overlayContainerElement.appendChild(overlayContentElement);
const overlay = new Overlay({
  element: overlayContainerElement,
  autoPan: true,
});
map.addOverlay(overlay);

// Function to add markers
function addMarkers(wells) {
  wells.forEach(well => {
    const feature = new Feature({
      geometry: new Point(fromLonLat([parseFloat(well.longitude), parseFloat(well.latitude)])),
      ...well
    });
    vectorSource.addFeature(feature);
  });
}

// Fetch and display oil wells data
fetch('http://localhost:3000/api/wells') // Make sure this URL matches your setup
  .then(response => response.json())
  .then(data => {
    const filteredWells = data.filter(well => well.longitude !== 'Unknown' && well.latitude !== 'Unknown');
    addMarkers(filteredWells);
    // Optionally, adjust the map view here based on the fetched markers
  })
  .catch(error => console.error('Error fetching data:', error));

// Handling click events to show popups
map.on('singleclick', function (evt) {
  const clickedFeature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });
  if (clickedFeature) {
    const {
      well_name,
      api_number,
      well_status,
      well_type,
      closest_city,
      barrels_of_oil,
      barrels_of_gas
    } = clickedFeature.getProperties();

    const popupContentHtml = `
      <h2>${well_name}</h2>
      <p><strong>API Number:</strong> ${api_number}</p>
      <p><strong>Status:</strong> ${well_status}</p>
      <p><strong>Type:</strong> ${well_type}</p>
      <p><strong>Closest City:</strong> ${closest_city}</p>
      <p><strong>Barrels of Oil:</strong> ${barrels_of_oil}</p>
      <p><strong>Barrels of Gas:</strong> ${barrels_of_gas}</p>
    `;
    overlayContentElement.innerHTML = popupContentHtml;
    overlay.setPosition(evt.coordinate);
  } else {
    overlay.setPosition(undefined);
  }
});
