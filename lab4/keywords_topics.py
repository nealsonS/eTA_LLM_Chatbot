import gensim #might use this, not sure
from transformers import AutoTokenizer, PegasusForConditionalGeneration


#example code from https://huggingface.co/docs/transformers/en/model_doc/pegasus

model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

# practice
ARTICLE_TO_SUMMARIZE = (
    "PG&E stated it scheduled the blackouts in response to forecasts for high winds "
    "amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were "
    "scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow."
)
inputs = tokenizer(ARTICLE_TO_SUMMARIZE, max_length=1024, return_tensors="pt")

# Generate Summary
summary_ids = model.generate(inputs["input_ids"])
tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]