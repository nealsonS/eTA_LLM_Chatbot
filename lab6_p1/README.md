Script Brief Overview

*****
NOTE TO TEAM: Please don't edit app.py directly with your code! 
Make a copy and work on your part, then we'll piece them together 
afterwards (trying to avoid merges and collisions)

Before running these code, make sure to follow all of the instructions in the README in /drive!
*****


In addition to the packages needed for the app.py, please also install:
- PyMuPDF Pillow


To run the code, go into the /drive folder and run
"streamlit run app.py"


Part 1 Scripts 

### pdf_extractor.py (complete)
	This extracts text and image content from PDF and inserts the data into MySQL database. Create a database and create a folder named "images" before running the script.
	Input:
	1. It asks user to input MySQL credentials and the path to the PDF file.
	Output:
	1. It puts all the extracted images into PNG format into /images.
	2. It inserts text content and image path files for each page into the database.


Inside /drive:

### app.py
	skeleton code from Lab 6 Google folder
	
	
### htmlTemplates.py
	skeleton code from Lab 6 Google folder
