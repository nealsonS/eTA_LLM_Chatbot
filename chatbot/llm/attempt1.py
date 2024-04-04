# source code from https://blog.devgenius.io/build-your-own-llm-model-using-openai-dd2be7fe9bb2

import pandas as pd
import numpy as np
import openai
from openai import OpenAI # for calling the OpenAI API
import torch
import os # for getting API token from env variable OPENAI_API_KEY
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))
data = pd.read_csv('winter_olympics_2022.csv')

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

MODEL_NAME = 'TheBloke/WizardLM-13B-V1.2-GGUF'
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

train_dataset = TextDataset(tokenizer=tokenizer, file_path='train_data.txt', block_size=128)

val_dataset = TextDataset(tokenizer=tokenizer, file_path='val_data.txt', block_size=128)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    eval_steps=100,
    save_steps=100,
    warmup_steps=10,
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)
trainer.train()

def generate_response(prompt, max_length=150, num_responses=1):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_responses,
        no_repeat_ngram_size=2,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    decoded_output = [tokenizer.decode(response, skip_special_tokens=True) for response in output]
    return decoded_output

prompt = "What are some strategies for effective marketing in the technology industry?"
responses = generate_response(prompt, num_responses=3)
for i, response in enumerate(responses):
    print(f"Response {i+1}: {response}\n")

