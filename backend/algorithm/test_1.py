from transformers import BertModel, BertTokenizer, AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import pandas as pd
from .model import *


def process_user_input(user_input):

	tokenizer = AutoTokenizer.from_pretrained("medicalai/ClinicalBERT")
	model = AutoModel.from_pretrained("medicalai/ClinicalBERT")
	# get model
	# model_name = 'bionlp/bluebert_pubmed_mimic_uncased_L-12_H-768_A-12'
	# tokenizer = BertTokenizer.from_pretrained(model_name)
	# model = BertModel.from_pretrained(model_name)

	def get_embedding(text):
		# make the inputs to id
		input_ids = tokenizer(text, return_tensors='pt')['input_ids']
		# get the outputs from bert
		with torch.no_grad():
			outputs = model(input_ids)
		return outputs.last_hidden_state[:, 0, :]

	# test case
	training = pd.read_csv('/Users/eeeeeeshen/Downloads/SP24/CS510/final project/CS510-Team8/backend/algorithm/Training.csv')

	# print("user input: ",user_input)
	# "I've been experiencing a persistent cough and mild fever over the last week. Initially, I thought it was just a common cold, but now I also have shortness of breath and occasional chest pains. I haven't been around anyone sick and I'm worried it might be something more serious. My energy levels are quite low and I've been feeling unusually tired."
	# user_input = "I have been dealing with severe headaches and dizziness for the past three days. It's worse in the morning. I also notice that my vision blurs occasionally, and I feel nauseous from time to time."
	symptoms = training.columns
	symptoms = symptoms[0:-1]
	keywords = symptoms.tolist()

	# get the embedding
	input_embed = get_embedding(user_input)
	keyword_embeds = [get_embedding(keyword) for keyword in keywords]

	# calculate the cosine similarity between all key words under bert model
	bert_scores = {keywords[i]: cosine_similarity(input_embed, keyword_embeds[i]).item() for i in range(len(keywords))}

	vectorizer = TfidfVectorizer()
	texts = [user_input] + keywords
	tfidf_matrix = vectorizer.fit_transform(texts)
	tfidf_array = tfidf_matrix.toarray()

	# calculate the tfidf score
	keyword_tfidf_scores = {keywords[i]: tfidf_array[0] @ tfidf_array[i + 1] for i in range(len(keywords))}

	# combine bert and tfidf score
	combined_scores = {}
	for keyword in keywords:
		combined_score = 0.5 * bert_scores[keyword] + 0.5 * keyword_tfidf_scores[keyword]
		combined_scores[keyword] = combined_score

	# sort the keywords
	sorted_keywords = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:5]

	result_list = []
	for keyword, score in sorted_keywords:
		result_list.append(keyword)
		print(f"{keyword}: {score}")
	return result_list