import gensim
from gensim.summarization import keywords

text = """spaCy is an open-source software library for advanced natural language processing, 
written in the programming languages Python and Cython. The library is published under the MIT license 
and its main developers are Matthew Honnibal and Ines Montani, the founders of the software company Explosion."""
print(keywords(text))



# example code below from https://huggingface.co/docs/transformers/en/model_doc/pegasus
# from transformers import AutoTokenizer, PegasusForConditionalGeneration #might use this, not sure
# model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
# tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
# # practice
# ARTICLE_TO_SUMMARIZE = (
#     "PG&E stated it scheduled the blackouts in response to forecasts for high winds "
#     "amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were "
#     "scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow."
# )
# inputs = tokenizer(ARTICLE_TO_SUMMARIZE, max_length=1024, return_tensors="pt")
# # Generate Summary
# summary_ids = model.generate(inputs["input_ids"])
# tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]