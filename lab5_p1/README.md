# Pre-running:
Please add the pdfs to the folder: data/raw/
RUN !pip install -r requirements.txt
	This install all the dependencies for this lab
	
RUN !sudo apt-get install tesseract-ocr
	This installs the tesseract-ocr package that the python wrapper `pytesseract` uses

