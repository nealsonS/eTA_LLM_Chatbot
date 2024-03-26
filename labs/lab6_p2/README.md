Script Brief Overview

*****
Before running these code, make sure to follow all of the instructions in the README in /drive!
*****

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

Please also do
pip install PyMuPDF Pillow sentence-transformers faiss-cpu



Part 2 Scripts 

Inside /drive:

To run the code, go into the /drive folder and run
"streamlit run app.py"

### app.py
	Our code built on the skeleton code from Lab 6 Google folder. We adjusted the code since part 1 for better performance.
	Takes the PDF file, extracts information, chunks it, puts it into vector data store.
	Allows users to ask questions about the PDF file they uploaded.
	Note: For faster performance testing, use doc1, doc2, and/or doc3 when running the application.
	
	
### htmlTemplates.py
	Contains the CSS styles for app.py

### skeleton.py
	skeleton code from Lab 6 Google folder




Inside /sandbox:

### pdf_extractor.py 
	This extracts text and image content from PDF and inserts the data into MySQL database. Create a database and create a folder named "images" before running the script.
	Input:
	1. It asks user to input MySQL credentials and the path to the PDF file.
	Output:
	1. It puts all the extracted images into PNG format into /images.
	2. It inserts text content and image path files for each page into the database.

### llm.py
	Input:
	1. It asks user to input MySQL credentials and the path to the PDF file.
	Process:
	1. makes text chunks of data
	2. puts chunks into vector store
	3. uses HuggingFace sentence-transformer instead of OpenAI
