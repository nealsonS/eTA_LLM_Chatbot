Script Brief Overview:

(This is for Part 2. Please scroll down to see information about Part 1 Scripts.)


Part 2 Scripts

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



	
	
	

Part 1 Scripts
### pdf_extraction.py
	Please download the data and change the pdf_directory variable to the path of local data
	
	Run this script to convert local pdf to text and extract useful information from the text.
	
	Input:
	1. It asks user to input login to mysql server
	Output: 
	1. Stores extracted data (well name, api number, longitude, latitude, address) into designated table in mysql server

### web_scraping.py
	Run this script after running pdf_extraction.py
 
	This script extracts api number stored in the database and use that to scrape more information about the well.
	
	Input:
	1. It asks user to input login to mysql server
	Output: 
	1. Stores extracted data (well status, well type, closest city, barrels of oil, barrels of gas, with updated well name) into designated table in mysql server


