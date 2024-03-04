Script Brief Overview:

(This is for Part 2. Please scroll down to see information about Part 1 Scripts.)


Part 2 Scripts
	
### my-app
In your terminal, run the following
	npm create ol-app my-app
	cd my-app
	npm start
The following scripts are inside the my-app folder.


###### map_display.py
	** underconstruction **
	Script connects to the MySQL database to retrieve well data information,
	then push the information to main.js to create pins on Map.
	Currently gets syntax error about modules / import in main.js.
	Considering to not use this at all

###### main.js
	creates map, pins, and map information via OpenLayers
	
###### needs_work_main.js
	tries to combine main.js with promises.js, and is not working
	
###### promises.js
	js code that connects to MySQL database and saves the collected data into an array to be processed and displayed in main.js.
	currently is not connecting.
	A working version of promises.js is in the SANDBOX folder and should be run using connect.js.

###### connect.js
	js code that exports the data promises.js is able to get.
	A working version of connect.js is in the SANDBOX folder. Run this to see how promises.js is supposed to work
	
###### index.html
	HTML doc that allows the map, pins, and information appear.

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


