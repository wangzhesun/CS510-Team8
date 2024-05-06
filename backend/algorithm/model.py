import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import json
from json import JSONEncoder
from .test_1 import *


dataset_path = '/Users/eeeeeeshen/Downloads/SP24/CS510/final project/CS510-Team8/backend/algorithm/Training.csv'
KN_pkl_path = "/Users/eeeeeeshen/Downloads/SP24/CS510/final project/CS510-Team8/backend/algorithm/KN.pkl"
def set_list(train_file):
        training = pd.read_csv(train_file)
        X = training.iloc[:,:-1]
        y = training.iloc[:,-1]
        le = LabelEncoder()
        le.fit(y)
        Y = le.transform(y)
        sympton_list = training.columns
        sympton_list = list(sympton_list.values)
        # print(sympton_list)
        disease_list = le.classes_
        # print(disease_list)
        return sympton_list, disease_list

sympton_list, disease_list = set_list(dataset_path)

class ModelName:
    def __init__(self):
        self.variable = 1
        self.query = None

    def predict(self,user_input_sym):
        KN = pickle.load(open(KN_pkl_path,'rb'))
        input_vector = np.zeros(len(sympton_list)-1)
        for sym in user_input_sym:
            if sym in sympton_list:
                index = sympton_list.index(sym)
                input_vector[index] = 1
        pre_dis_index = KN.predict([input_vector])
        disease = disease_list[pre_dis_index]
        # print(pre_dis)
        return disease

    def analyze(self, query):
        
        self.query = query
        processed_user_symptoms = process_user_input(query)
        # user_symptoms = processed_user_symptoms.split(",")
        user_symptoms = [sym.strip() for sym in processed_user_symptoms]
        print(processed_user_symptoms)
        print(user_symptoms)
        model = ModelName()
        predicted_disease = model.predict(user_symptoms)
        print(predicted_disease)
        result = predicted_disease.tolist()
        
        return result[0]
