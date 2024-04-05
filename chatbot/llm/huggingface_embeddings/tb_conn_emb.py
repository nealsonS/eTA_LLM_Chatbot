# source code from https://huggingface.co/blog/getting-started-with-embeddings

import requests
import torch
from datasets import load_dataset
from sentence_transformers.util import semantic_search
import fitz  # PyMuPDF


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
        

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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" #read, called chatbot_1

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}


tb_embeddings = load_dataset('DHO560/practice_tb_embedding_dataset')
dataset_embeddings = torch.from_numpy(tb_embeddings["train"].to_pandas().to_numpy()).to(torch.float)

question = ["What are quality assessments for drug therapy?"]
output = query(question)
#print(output)

query_embeddings = torch.FloatTensor(output)

hits = semantic_search(query_embeddings, dataset_embeddings, top_k=5)
print(hits[0]) #is a list. hits would give a list in a list
## util.semantic_search identifies how close each of the pages is to the customer query and returns a list of dictionaries with the top top_k 
# looks like
#[[{'corpus_id': 489, 'score': 0.6776377558708191}, 
#{'corpus_id': 503, 'score': 0.5736414194107056}, #not page numbers!
#{'corpus_id': 643, 'score': 0.566224992275238}, 
#{'corpus_id': 196, 'score': 0.563490092754364}, 
#{'corpus_id': 25, 'score': 0.5421655178070068}]]


pdf_path = '/home/vboxuser/chatbot/raw_course_materials/textbook.pdf' #adjust as needed
texts = extract_content_from_pdf(pdf_path)
print([texts[hits[0][i]['corpus_id']] for i in range(len(hits[0]))])
## values ​​in corpus_id allow us to index the list of texts we defined in the first section and get the five most similar FAQs

