from transformers import BertModel, BertTokenizer, AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import pandas as pd
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize

# Download the necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

threshold = 0.69



def process_user_input(user_input):
	potential_keywords = set()
	final_keywords = set()
	# Define a function to check if a phrase is meaningful
	def is_meaningful(phrase):
		words = nltk.word_tokenize(phrase)
		pos_tags = nltk.pos_tag(words)
		
		# Check if the phrase contains at least one meaningful word
		# meaningful_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
		meaningful_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBN', 'VBZ']
		# remove 'vbp' , 'VBG','JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'
		
		if len(words) == 1:
			word = words[0]
			tag = pos_tags[0][1]
			# print(word,tag)
			return tag in meaningful_tags and word.lower() not in stop_words
		else:
			return any(tag in meaningful_tags for word, tag in pos_tags)




	def chunk_sentence(sentence):
		# Tokenize the sentence into words
		words = word_tokenize(sentence)

		# Define the grammar for chunking
		grammar = r"""
			NP: {<DT|JJ|NN.*>+}  # Noun Phrase
			PP: {<IN><NP>}       # Prepositional Phrase
			VP: {<VB.*><NP|PP>*} # Verb Phrase
		"""

		# Create a chunk parser
		chunk_parser = nltk.RegexpParser(grammar)

		# Part-of-speech tag the words
		tagged_words = nltk.pos_tag(words)

		# Chunk the tagged words
		tree = chunk_parser.parse(tagged_words)

		# Extract phrases from the parse tree
		phrases = []
		for subtree in tree.subtrees(filter=lambda t: t.label() != 'S'):
			phrase = ' '.join([word for word, tag in subtree.leaves()])
			phrases.append(phrase)

		return phrases



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
	# user_input = "I've been experiencing a persistent cough and mild fever over the last week. Initially, I thought it was just a common cold, but now I also have shortness of breath and occasional chest pains. I haven't been around anyone sick and I'm worried it might be something more serious. My energy levels are quite low and I've been feeling unusually tired."

	# user_input = "I've been experiencing a persistent cough and mild fever over the last week. "
	seg_user_input=chunk_sentence(user_input)

	# Define a set of stopwords
	stop_words = set(stopwords.words('english'))

	# Filter out less meaningful phrases
	meaningful_user_input = [phrase for phrase in seg_user_input if is_meaningful(phrase)]


	# user_input = "I have been dealing with severe headaches and dizziness for the past three days. It's worse in the morning. I also notice that my vision blurs occasionally, and I feel nauseous from time to time."
	symptoms = training.columns
	symptoms = symptoms[0:-1]
	# keywords = symptoms.tolist()
	keywords = [symptom.replace('_', ' ') for symptom in symptoms]

	input_embeds = [get_embedding(text) for text in meaningful_user_input]
	keyword_embeds = [get_embedding(keyword) for keyword in keywords]

	bert_scores_list = []
	keyword_tfidf_scores_list = []
	combined_scores_list = []

	for j in range(len(input_embeds)):
		bert_scores = {keywords[i]: cosine_similarity(input_embeds[j], keyword_embeds[i]).item() for i in range(len(keywords))}
		bert_scores_list.append(bert_scores)
		
		texts = [seg_user_input[j]] + keywords
		vectorizer = TfidfVectorizer()
		tfidf_matrix = vectorizer.fit_transform(texts)
		tfidf_array = tfidf_matrix.toarray()
		keyword_tfidf_scores = {keywords[i]: tfidf_array[0] @ tfidf_array[i + 1] for i in range(len(keywords))}
		keyword_tfidf_scores_list.append(keyword_tfidf_scores)
		
		combined_scores = {}
		for keyword in keywords:
			combined_score = 0.7 * bert_scores[keyword] + 0.3 * keyword_tfidf_scores[keyword]
			# combined_score = 1.0 * bert_scores[keyword] 
			combined_scores[keyword] = combined_score
		combined_scores_list.append(combined_scores)

	for j in range(len(input_embeds)):
		print(f"Input {j+1}:")
		sorted_keywords = sorted(combined_scores_list[j].items(), key=lambda x: x[1], reverse=True)[:2]
		for keyword, score in sorted_keywords:
			print(f"{keyword}: {score}")
			potential_keywords.add(keyword)
			if score > threshold:
				final_keywords.add(keyword)
		print()

	if not final_keywords:
		final_keywords = potential_keywords
	final_keywords = {keyword.replace(' ', '_') for keyword in final_keywords}
	print(final_keywords)
	return final_keywords