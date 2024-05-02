import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('/home/vboxuser/chatbot/llm/huggingface_embeddings/course_materials_embeddings_4_9.csv', header=None, names=['embedding'])

# Reshape the DataFrame to have a single cell containing all values
df_cell = str(df['embedding']).str.cat(sep=', ')

# Display the DataFrame cell
print(df_cell)
df_cell.to_csv("cme_v1.csv", index=False)
