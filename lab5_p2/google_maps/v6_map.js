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
  const center = { lat: 48.11, lng: -103.73 };
  const map = new Map(document.getElementById("map"), {
    zoom: 17,
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



