Script Brief Overview:

(This is for Part 2. Please scroll down to see information about Part 1 Scripts.)


Part 2 Scripts
Please download 

### my-app
In your terminal, run the following
	npm create ol-app my-app
	cd my-app
	npm start


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


