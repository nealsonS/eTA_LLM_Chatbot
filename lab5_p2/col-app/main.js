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
import {Icon, Style} from 'ol/style';
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
});

map.addLayer(vectorLayer);

// Create an overlay for popups
const overlayContainerElement = document.createElement('div');
overlayContainerElement.className = 'overlay-container';
const overlayLayer = new Overlay({
  element: overlayContainerElement,
  autoPan: true,
});
map.addOverlay(overlayLayer);

// Function to add markers
function addMarkers(wells) {
  wells.forEach(well => {
    const feature = new Feature({
      geometry: new Point(fromLonLat([well.longitude, well.latitude])),
      name: well.name,
    });
    feature.setStyle(new Style({
      image: new Icon({
        src: '/path/to/marker-icon.png', // Use your marker icon
        scale: 0.05, // Adjust as necessary
      }),
    }));
    vectorSource.addFeature(feature);
  });
}

// Fetch and display oil wells data
fetch('http://localhost:3000/api/wells') // Update with the correct URL
  .then(response => response.json())
  .then(data => {
    addMarkers(data);
    // Optionally, adjust the map view here based on the fetched markers
  })
  .catch(error => console.error('Error fetching data:', error));

// Handling click events to show popups
map.on('singleclick', function (evt) {
  const clickedFeature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });
  if (clickedFeature) {
    const featureProps = clickedFeature.getProperties();
    overlayContainerElement.innerHTML = `<div class="popup-content">Name: ${featureProps.name}</div>`; // Customize as needed
    overlayLayer.setPosition(evt.coordinate);
  } else {
    overlayLayer.setPosition(undefined);
  }
});
