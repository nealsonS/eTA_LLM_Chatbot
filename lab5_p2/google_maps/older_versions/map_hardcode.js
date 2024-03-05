async function initMap() {
  // Request needed libraries.
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const center = { lat: 37.43238031167444, lng: -122.16795397128632 };
  const map = new Map(document.getElementById("map"), {
    zoom: 11,
    center,
    mapId: "4504f8b37365c3d0",
  });

  for (const place of places) {
    const AdvancedMarkerElement = new google.maps.marker.AdvancedMarkerElement({
      map,
      content: buildContent(place),
      position: place.position,
      title: place.description,
    });

    AdvancedMarkerElement.addListener("click", () => {
      toggleHighlight(AdvancedMarkerElement, place);
    });
  }
}

function toggleHighlight(markerView, place) {
  if (markerView.content.classList.contains("highlight")) {
    markerView.content.classList.remove("highlight");
    markerView.zIndex = null;
  } else {
    markerView.content.classList.add("highlight");
    markerView.zIndex = 1;
  }
}

function buildContent(place) {
  const content = document.createElement("div");

  content.classList.add("place");
  content.innerHTML = `
    <div class="icon">
        <i aria-hidden="true" class="fa fa-icon fa-${place.well_type}" title="${place.well_type}"></i>
        <span class="fa-sr-only">${place.well_type}</span>
    </div>
    <div class="details">
        <div class="well_status">${place.well_status}</div>
        <div class="address">${place.address}</div>
        <div class="features">
        <div>
            <i aria-hidden="true" class="fa fa-closest_city fa-lg closest_city" title="closest_city"></i>
            <span class="fa-sr-only">closest_city</span>
            <span>${place.closest_city}</span>
        </div>
        <div>
            <i aria-hidden="true" class="fa fa-barrels_of_oil fa-lg barrels_of_oil" title="barrels_of_oil"></i>
            <span class="fa-sr-only">barrels_of_oil</span>
            <span>${place.barrels_of_oil}</span>
        </div>
        <div>
            <i aria-hidden="true" class="fa fa-ruler fa-lg barrels_of_gas" title="barrels_of_gas"></i>
            <span class="fa-sr-only">barrels_of_gas</span>
            <span>${place.barrels_of_gas} ft<sup>2</sup></span>
        </div>
        </div>
    </div>
    `;
  return content;
}


// This is hardcoded from existing mysql table
const places = [
  {
    address: '1001 Fannin,Sulte 1 500',
    well_name: 'Lewis Federal 5300 11-31 3B',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '1.9 k',
    barrels_of_gas: '5.7 k',
    position: { lat: 48.03581, lng: 103.602608 },
  },
  {
    address: 'D Drilling Prognosis \n' +
      'D Redrilling or Repair \n' +
      'D Casing or Liner \n' +
      'D PlugWell \n' +
      'D Supplemental History \n' +
      'D Temporarily Abandon \n' +
      'D Other \n' +
      'I Township \n' +
      '153 N I Range \n' +
      '101 w \n' +
      'I County \n' +
      'Williams \n' +
      'lCity \n' +
      'DETAILS OF WORK D \n' +
      'D',
    well_name: 'Atlanta 3-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '429',
    barrels_of_gas: '725',
    position: { lat: 48.1094, lng: -103.7312 },
  },
  {
    address: 'I I I \nI I I \nI',
    well_name: 'Atlanta 4-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '348',
    barrels_of_gas: '627',
    position: { lat: 48.1094, lng: -103.7329 },
  },
  {
    address: 'on the reverse \nso that we can return the card to you',
    well_name: 'Buck Shot SWD 5300 31-31',
    well_status: 'Active',
    well_type: 'Salt Water Disposal',
    closest_city: 'Williston',
    barrels_of_oil: 'Not available',
    barrels_of_gas: 'Not available',
    position: { lat: 48.02, lng: 103.35 },
  },
  {
    address: 'D \n' +
      'D \n' +
      'D Casing or Liner \n' +
      'D PlugWell \n' +
      'D Supplemental History \n' +
      'D Temporarily Abandon \n' +
      '0 Other \n' +
      'I Township \n' +
      '153 N I Range \n' +
      '101 w \n' +
      'I County \n' +
      'Williams \n' +
      'lCity \n' +
      'DETAILS OF WORK Oil \n' +
      'Water \n' +
      'Gas',
    well_name: 'Atlanta 11-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '731',
    barrels_of_gas: '1.1 k',
    position: { lat: 48.11, lng: -103.73 },
  },
  {
    address: 'O Drilling Prognosis \n' +
      '0 Redrilling or Repair \n' +
      '0 Casing or Liner \n' +
      'O PlugWell \n' +
      'O Supplemental History \n' +
      'D Temporarily Abandon \n' +
      '0 Other \n' +
      'I Township \n' +
      '153 N I Range \n' +
      '101 w I County \n' +
      'Williams \n' +
      'I City \n' +
      'DETAILS OF WORK Oil \n' +
      'Water \n' +
      'Gas D \n' +
      'D',
    well_name: 'Atlanta 12-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '236',
    barrels_of_gas: '493',
    position: { lat: 48.109, lng: -103.728 },
  },
  {
    address: '',
    well_name: 'Atlanta 1-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '947',
    barrels_of_gas: '1.4 k',
    position: { lat: 48.11, lng: -103.73 },
  },
  {
    address: 'D \n' +
      'D Redrilling or Repair \n' +
      'D Casing or Liner \n' +
      'D Plug Well \n' +
      'D Supplemental History \n' +
      'D Temporarily Abandon \n' +
      'D Other \n' +
      'I Township \n' +
      '153 N I Range \n' +
      '101 w I County \n' +
      'Williams \n' +
      'DETAILS OF WORK Oil \n' +
      'Water \n' +
      'Gas D \n' +
      'D IWell File No',
    well_name: 'Atlanta 13-6H',
    well_status: 'Active',
    well_type: 'Oil & Gas',
    closest_city: 'Williston',
    barrels_of_oil: '708',
    barrels_of_gas: '1.1 k',
    position: { lat: 48.109, lng: -103.728 },
  },
];


initMap();



