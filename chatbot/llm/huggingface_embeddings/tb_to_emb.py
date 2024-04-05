import requests
import pandas as pd
import fitz  # PyMuPDF


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



pdf_path = '/home/vboxuser/chatbot/raw_course_materials/textbook.pdf' #adjust as needed
texts = extract_content_from_pdf(pdf_path)
print(texts)
print(len(texts)) # should be 649, same number of pages as textbook.pdf

output = query(texts)
print(output)
print(len(output)) # should be 649, same number of pages as textbook.pdf

embeddings = pd.DataFrame(output)
embeddings.to_csv("tb_embeddings.csv", index=False)

