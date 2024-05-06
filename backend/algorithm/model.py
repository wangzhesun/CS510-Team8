import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle
import json
from json import JSONEncoder


dataset_path = './backend/algorithm/Training.csv'
KN_pkl_path = "./backend/algorithm/KN.pkl"
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
        user_symptoms = query.split(",")
        user_symptoms = [sym.strip() for sym in user_symptoms]

        print(user_symptoms)
        model = ModelName()
        predicted_disease = model.predict(user_symptoms)
        print(predicted_disease)
        result = predicted_disease.tolist()
        # result = json.dumps({"": predicted_disease.tolist()})
        # result = JSONEncoder.default(self, result)
        return result[0]
