# imports
import ast  # for converting embeddings saved as strings back to arrays
from openai import OpenAI # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import os # for getting API token from env variable OPENAI_API_KEY
from scipy import spatial  # for calculating vector similarities for search


# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo" # or "gpt-4"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))

# an example question about the 2022 Olympics
query = 'Which athletes won the gold medal in curling at the 2022 Winter Olympics?'


response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'You answer questions about the 2022 Winter Olympics.'},
        {'role': 'user', 'content': query},
    ],
    model=GPT_MODEL,
    temperature=0,
)

print(response.choices[0].message.content)
