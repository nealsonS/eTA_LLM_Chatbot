// Fetch and display oil wells data
fetch('http://localhost:3000/api/wells') // Make sure this URL matches your setup
  .then(response => response.json())
  .then(data => {
    const places = data.filter(well => well.longitude !== 'Unknown' && well.latitude !== 'Unknown');
    //addMarkers(filteredWells);
    // Optionally, adjust the map view here based on the fetched markers
    console.log(places);
    initMap(places);
  })
  .catch(error => console.error('Error fetching data:', error));



async function initMap(places) {
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
      position: new google.maps.LatLng(place.latitude, place.longitude),
      //position:{lat: place.latitude, lng: place.longitude}
      //position: place.position,
      title: place.well_name,
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

# This is hardcoded from existing mysql table
const hardcoded_places = [
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


const places1 = [
  {
    address: "address",
    well_name: "Single family house with modern design",
    well_status: "$ 3,889,000",
    well_type: "home",
    closest_city: 5,
    barrels_of_oil: 4.5,
    barrels_of_gas: 300,
    position: {
      lat: 37.50024109655184,
      lng: -122.28528451834352,
    },
  },
  {
    address: "108 Squirrel Ln &#128063;, Menlo Park, CA",
    well_name: "Townhouse with friendly neighbors",
    well_status: "$ 3,050,000",
    well_type: "building",
    closest_city: 4,
    barrels_of_oil: 3,
    barrels_of_gas: 200,
    position: {
      lat: 37.44440882321596,
      lng: -122.2160620727,
    },
  },
  {
    address: "100 Chris St, Portola Valley, CA",
    well_name: "Spacious warehouse great for small business",
    well_status: "$ 3,125,000",
    well_type: "warehouse",
    closest_city: 4,
    barrels_of_oil: 4,
    barrels_of_gas: 800,
    position: {
      lat: 37.39561833718522,
      lng: -122.21855116258479,
    },
  },
  {
    address: "98 Aleh Ave, Palo Alto, CA",
    well_name: "A lovely store on busy road",
    well_status: "$ 4,225,000",
    well_type: "store-alt",
    closest_city: 2,
    barrels_of_oil: 1,
    barrels_of_gas: 210,
    position: {
      lat: 37.423928529779644,
      lng: -122.1087629822001,
    },
  },
  {
    address: "2117 Su St, MountainView, CA",
    well_name: "Single family house near golf club",
    well_status: "$ 1,700,000",
    well_type: "home",
    closest_city: 4,
    barrels_of_oil: 3,
    barrels_of_gas: 200,
    position: {
      lat: 37.40578635332598,
      lng: -122.15043378466069,
    },
  },
  {
    address: "197 Alicia Dr, Santa Clara, CA",
    well_name: "Multifloor large warehouse",
    well_status: "$ 5,000,000",
    well_type: "warehouse",
    closest_city: 5,
    barrels_of_oil: 4,
    barrels_of_gas: 700,
    position: {
      lat: 37.36399747905774,
      lng: -122.10465384268522,
    },
  },
  {
    address: "700 Jose Ave, Sunnyvale, CA",
    well_name: "3 storey townhouse with 2 car garage",
    well_status: "$ 3,850,000",
    well_type: "building",
    closest_city: 4,
    barrels_of_oil: 4,
    barrels_of_gas: 600,
    position: {
      lat: 37.38343706184458,
      lng: -122.02340436985183,
    },
  },
  {
    address: "868 Will Ct, Cupertino, CA",
    well_name: "Single family house in great school zone",
    well_status: "$ 2,500,000",
    well_type: "home",
    closest_city: 3,
    barrels_of_oil: 2,
    barrels_of_gas: 100,
    position: {
      lat: 37.34576403052,
      lng: -122.04455090047453,
    },
  },
  {
    address: "655 Haylee St, Santa Clara, CA",
    well_name: "2 storey store with large storage room",
    well_status: "$ 2,500,000",
    well_type: "store-alt",
    closest_city: 3,
    barrels_of_oil: 2,
    barrels_of_gas: 450,
    position: {
      lat: 37.362863347890716,
      lng: -121.97802139023555,
    },
  },
  {
    address: "2019 Natasha Dr, San Jose, CA",
    well_name: "Single family house",
    well_status: "$ 2,325,000",
    well_type: "home",
    closest_city: 4,
    barrels_of_oil: 3.5,
    barrels_of_gas: 500,
    position: {
      lat: 37.41391636421949,
      lng: -121.94592071575907,
    },
  },
];


