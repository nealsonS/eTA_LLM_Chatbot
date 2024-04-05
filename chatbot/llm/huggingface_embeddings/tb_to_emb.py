import requests
import pandas as pd
import fitz  # PyMuPDF
import os

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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" #read, called chatbot_1


api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}


def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()


def extract_content_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    try:
        text_pages = []
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text_pages.append(page.get_text("text") + " ")
        return text_pages
    finally:
        doc.close()



pdf_directory = '/home/vboxuser/chatbot/all_course_materials/' #adjust as needed

all_materials = []

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        #extract text content and images
        texts = extract_content_from_pdf(pdf_path)
        print(len(texts)) # should be 649, same number of pages as textbook.pdf
        all_materials.append(texts)
        print(f"Extracted text for '{filename}'")

all_outputs = []
for texts in all_materials:
    output = query(texts)
    #print(output)
    print(len(output)) # should be 649, same number of pages as textbook.pdf
    all_outputs.append(output)

for a in range(len(all_outputs)): #need to fix this
    if a == 0:
        df = pd.DataFrame(all_outputs[a])
    else:
        df_new_rows = pd.DataFrame(all_outputs[a]
        embeddings = pd.concat([df, df_new_rows])

embeddings.to_csv("course_materials_embeddings_v1.csv", index=False)

