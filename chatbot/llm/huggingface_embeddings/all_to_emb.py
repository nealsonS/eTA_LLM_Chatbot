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
print("Extracting data from PDFs...")
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        #extract text content and images
        texts = extract_content_from_pdf(pdf_path)
        #print(len(texts)) # should be 649, same number of pages as textbook.pdf
        all_materials.append(texts)
        #print(f"Extracted text for '{filename}'")

print("Creating embeddings, DO NOT INTERRUPT...")
all_outputs = []
for texts in all_materials:
    output = query(texts)
    #print(output)
    #print(len(output)) # should be same number of pages as each PDF
    all_outputs.append(output)

print("Storing embeddings, DO NOT INTERRUPT...")
#for a in range(len(all_outputs)): 
#    if a == 0:
#        df = pd.DataFrame(all_outputs[a])
        #print(len(df))
#    else:
#        df_new_rows = pd.DataFrame(all_outputs[a])
#        df = pd.concat([df, df_new_rows])     
#        if a == len(all_outputs)-1: #the last thing to add
#            df.to_csv("course_materials_embeddings_v3.csv", index=False)

df = pd.DataFrame()
for i in range(len(all_outputs)):
    embedding_str = ', '.join(map(str, all_outputs[i]))
    # Add the text and embedding string to a new DataFrame
    df_new = pd.DataFrame({'text': all_materials[i], 'embedding': embedding_str})
    # Concatenate the new DataFrame with the existing one
    df = pd.concat([df, df_new])

# Save the DataFrame to a CSV file
df.to_csv("course_materials_embeddings_4_10.csv", index=False)

print("Done.")
