import {Feature, Map, Overlay, View} from 'ol/index.js';
import {OSM, Vector as VectorSource} from 'ol/source.js';
import {Point} from 'ol/geom.js';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer.js';
import {useGeographic} from 'ol/proj.js';

useGeographic();

//DEFAULT CODE

//const place = [-110, 45]; 
//const place = [103.35, 48.02]; 
//const point = new Point(place);

//const map = new Map({
//  target: 'map',
//  view: new View({
//    center: place,
//    zoom: 8,
//  }),
//  layers: [
//    new TileLayer({
//      source: new OSM(),
//    }),
//    new VectorLayer({
//      source: new VectorSource({
//        features: [new Feature(point)],
//      }),
//      style: {
//        'circle-radius': 9,
//        'circle-fill-color': 'red',
//      },
//    }),
//  ],
//});

const places = [  
  [-103.73, 48.11],
  [-103.7329, 48.1094], 
  [103.602608, 48.03581],
  [-103.728, 48.109], 
  [-103.728, 48.109], 
  [103.35, 48.02], 
  [-103.73, 48.11], 
  [-103.7312, 48.1094]  
];

const features = places.map(place => {
  const point = new Point(place);
  return new Feature(point);
});

const map = new Map({
  target: 'map',
  view: new View({
    center: places[0],  // initial point 
    zoom: 13., // set zoom look out and see many points
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



function formatCoordinate(coordinate) {
  return `
    <table>
      <tbody>
        <tr><th>well name</th><td>NA</td></tr>
        <tr><th>longitude</th><td>${coordinate[0].toFixed(2)}</td></tr>
        <tr><th>latitude</th><td>${coordinate[1].toFixed(2)}</td></tr>
        <tr><th>address</th><td>NA</td></tr>
        <tr><th>well status</th><td>NA</td></tr>
        <tr><th>well type</th><td>NA</td></tr>
        <tr><th>closest city</th><td>NA</td></tr>
        <tr><th>barrel of oil</th><td>NA</td></tr>
        <tr><th>barrels of gas</th><td>NA</td></tr>
      </tbody>
    </table>`;
}

const info = document.getElementById('info');
map.on('moveend', function () {
  const view = map.getView();
  const center = view.getCenter();
  info.innerHTML = formatCoordinate(center);
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
  const coordinate = feature.getGeometry().getCoordinates();
  popup.setPosition([
    coordinate[0] + Math.round(event.coordinate[0] / 360) * 360,
    coordinate[1],
  ]);

  popover = new bootstrap.Popover(element, {
    container: element.parentElement,
    content: formatCoordinate(coordinate),
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

