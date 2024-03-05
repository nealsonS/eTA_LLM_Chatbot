  
  function initMap(places) {
    const center = { lat: 37.4323, lng: -122.1679 };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 11,
      center,
    });
  
    places.forEach(place => {
      const marker = new google.maps.Marker({
        map: map,
        position: { lat: parseFloat(place.latitude), lng: parseFloat(place.longitude) },
        title: place.well_name,
      });
  
      const infowindow = new google.maps.InfoWindow({
        content: buildContent(place),
      });
  
      marker.addListener('click', () => {
        infowindow.open(map, marker);
      });
    });
  }
  
  // Fetch and display oil wells data
  fetch('http://localhost:3000/api/wells')
    .then(response => response.json())
    .then(data => {
      const places = data.filter(well => well.longitude !== 'Unknown' && well.latitude !== 'Unknown').map(well => ({
        ...well,
        latitude: well.latitude,
        longitude: well.longitude,
      }));
      initMap(places); 
    })
    .catch(error => console.error('Error fetching data:', error));
  

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