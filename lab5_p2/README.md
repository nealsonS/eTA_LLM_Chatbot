Script Brief Overview:


Part 2 Scripts (assumes that Part 1 scripts were successfully run)

### conn_db (folder)
	In your terminal in your folder, run 
	"node server.js"
	This code should continue running in your background.

###### server.js
	working js code that exports the data from mysql.
	also listens for front-end to output this data.
	

### google_maps (folder)
	Please use Google Chrome to display the map
	In your terminal, run 
	"python3 -m http.server & xdg-open http://localhost:8000/v6_index.html"

	
###### v6_index.html
	HTML doc that allows the map, pins, and information appear.

###### v6_map.js
	creates map, pins, and map information via Google Maps API
	
###### v6_style.css
	styles for v6_map.js
	
###### package.json
	json file that contains dependencies for the map code to work


