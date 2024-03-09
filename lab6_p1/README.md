Script Brief Overview

*****
NOTE TO TEAM: Please don't edit app.py directly with your code! 
Make a copy and work on your part, then we'll piece them together 
afterwards (trying to avoid merges and collisions)

Before running these code, make sure to follow all of the instructions in the README in /drive!
*****


In addition to the packages needed for the app.py, please also install:
- pip install PyMuPDF Pillow sentence-transformer faiss-cpu

For this project, we will use Llama model because it's free.
Download it from here:
https://huggingface.co/TheBloke/LLaMa-7B-GGML/blob/main/llama-7b.ggmlv3.q4_1.bin and place it in the models folder

For embedding, we use HuggingFace sentence-transformer
**DISCLAIMER**:
This model has been quantized in a GGML format, but llama-cpp-python package only supports 
GGUF format past version 0.1.78.
Please downgrade to llama-cpp-python version 0.1.78 instead!
Run: pip install llama-cpp-python==0.1.78
For more information: https://huggingface.co/TheBloke/Llama-2-13B-GGML/discussions/5#64e9f825646192530130bc4c



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

### chunk.py
	Initial testing of chunk. Still WIP
	Input:
	1. no input, make sure MySQL credentials are correct before running
	Output:
	1. text chunks of data

Inside /drive:

### app.py
	skeleton code from Lab 6 Google folder
	NOTE: we should put all of our working code here!
	
	
### htmlTemplates.py
	skeleton code from Lab 6 Google folder
