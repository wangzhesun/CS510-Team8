from transformers import BertModel, BertTokenizer
import torch
import pandas as pd

# get model
model_name = 'bionlp/bluebert_pubmed_mimic_uncased_L-12_H-768_A-12'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def get_embedding(text):
	# make the inputs to id
	input_ids = tokenizer(text, return_tensors='pt')['input_ids']
	# get the outputs from bert
	with torch.no_grad():
		outputs = model(input_ids)
	return outputs.last_hidden_state[:, 0, :]

# test case
training = pd.read_csv('Training.csv')
user_input = "I've been experiencing a persistent cough and mild fever over the last week. Initially, I thought it was just a common cold, but now I also have shortness of breath and occasional chest pains. I haven't been around anyone sick and I'm worried it might be something more serious. My energy levels are quite low and I've been feeling unusually tired."
symptoms = training.columns
symptoms = symptoms[0:-1]
keywords = symptoms.tolist()

# get the embedding
input_embed = get_embedding(user_input)
keyword_embeds = [get_embedding(keyword) for keyword in keywords]

from sklearn.metrics.pairwise import cosine_similarity

# calculate the cosine similarity between all key words
similarity_scores = [cosine_similarity(input_embed, keyword_embed).item() for keyword_embed in keyword_embeds]

# get the similarity scores
keyword_similarity = list(zip(keywords, similarity_scores))

# sort the keywords
sorted_keywords = sorted(keyword_similarity, key=lambda x: x[1], reverse=True)

for keyword, score in sorted_keywords:
	print(f"{keyword}: {score}")
