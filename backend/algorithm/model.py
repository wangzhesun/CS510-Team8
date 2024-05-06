import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle

def read_file(train_file,test_file):
	training = pd.read_csv(train_file)
	testing = pd.read_csv(test_file)
	return training

read_file('./backend/algorithm/Training.csv',
		  "./backend/algorithm/Testing.csv")

def get_predicted_value(user_input_sym):
	KN = pickle.load(open('./backend/algorithm/KN.pkl','rb'))
	training = read_file('./backend/algorithm/Training.csv',"./backend/algorithm/Testing.csv")
	sympton_list = training.columns
	sympton_list = list(sympton_list.values)
	y = training.iloc[:,-1]
	le = LabelEncoder()
	le.fit(y)
	disease_list = le.classes_
		
	input_vector = np.zeros(len(sympton_list)-1)
	for sym in user_input_sym:
		if sym in sympton_list:
			index = sympton_list.index(sym)
			input_vector[index] = 1
	pre_dis_index = KN.predict([input_vector])
	disease = disease_list[pre_dis_index]
	# print(disease)
	
	return disease


class ModelName:
	def __init__(self):
		self.variable = 1
		
	# add models and other helper function

	def analyze(self, query):
		user_symptoms = query.split(",")
		# return user_symptoms
		disease = get_predicted_value(user_symptoms)
		# return user_symptoms
		# print(disease)
		disease_tolist = disease.tolist()
		# print(disease)
		# print(disease[0])
		# print(type(query))
		# print(type(disease[0]))
		# print(type(disease_tolist))
		# return query
		return disease_tolist[0]
