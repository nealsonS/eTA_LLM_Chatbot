# imports
import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search
import fitz  # PyMuPDF
#from transformers import GPT2Tokenizer
# for embeddings
#tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-2.7B")


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


# models
EMBEDDING_MODEL = "text-embedding-ada-002"
#GPT_MODEL = "gpt-3.5-turbo" 
GPT_MODEL = "gpt-4"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))


# For 1 TXT file
# text from: https://en.wikipedia.org/wiki/Curling_at_the_2022_Winter_Olympics
#with open("wikipedia_curling.txt", "r", encoding="utf-8") as file:
#    article = file.read()

## For 1 PDF
#pdf_path = '/home/vboxuser/chatbot/llm/wikipedia_curling.pdf'
pdf_path = '/home/vboxuser/chatbot/all_course_materials/wikip.pdf' # too big for gpt-4! tokens, not num of words
pdf_path = '/home/vboxuser/chatbot/all_course_materials/textbook.pdf' # too big for gpt-4!
article = extract_content_from_pdf(pdf_path)


## For folders of materials
#pdf_directory = '/home/vboxuser/chatbot/llm/' #adjust as needed
#all_materials = []
#print("Extracting data from PDFs...")
#for filename in os.listdir(pdf_directory):
#    if filename.endswith('.pdf'):
#        pdf_path = os.path.join(pdf_directory, filename)
        #extract text content and images
#        texts = extract_content_from_pdf(pdf_path)
        #print(len(texts))
#        for i in range(len(texts)):
#            all_materials.append(texts[i])
        #print(f"Extracted text for '{filename}'")



query = f"""Use the below article to answer the subsequent question. If the answer cannot be found, write "I don't know."

Article:
\"\"\"
{article}
\"\"\"

Question: What are the quality assessments of drug therapy?"""

#print(query)

response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about the textbook.'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL, # cannot use embeddings to shrink doc input, since model uses natural language text
    temperature=0,
)

print(response.choices[0].message.content)
