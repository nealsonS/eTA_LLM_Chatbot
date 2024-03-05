// Fetch and display oil wells data
fetch('http://localhost:3000/api/wells') // Make sure this URL matches your setup
  .then(response => response.json())
  .then(data => {
    const places = data.filter(well => well.longitude !== 'Unknown' && well.latitude !== 'Unknown');
    //addMarkers(filteredWells);
    // Optionally, adjust the map view here based on the fetched markers
    console.log(places);
  })
  .catch(error => console.error('Error fetching data:', error));



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


initMap();

