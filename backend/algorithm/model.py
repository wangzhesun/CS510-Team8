import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle

def set_list(train_file,test_file):
    training = pd.read_csv(train_file)
    testing = pd.read_csv(test_file)
    X = training.iloc[:,:-1]
    y = training.iloc[:,-1]
    le = LabelEncoder()
    le.fit(y)
    Y = le.transform(y)
    sympton_list = training.columns
    sympton_list = list(sympton_list.values)
    print(sympton_list)
    disease_list = le.classes_
    print(disease_list)
    return sympton_list, disease_list

def predict(user_input_sym):
    KN = pickle.load(open('KN.pkl','rb'))
    input_vector = np.zeros(len(sympton_list)-1)
    for sym in user_input_sym:
        if sym in sympton_list:
            index = sympton_list.index(sym)
            input_vector[index] = 1
    pre_dis_index = KN.predict([input_vector])
    disease = disease_list[pre_dis_index]
    # print(pre_dis)
    return disease


    
sympton_list, disease_list = set_list('Training.csv',"Testing.csv")
# testing example
user_input = input("Enter your symptoms: ")
user_symptoms = user_input.split(",")
user_symptoms = [sym.strip() for sym in user_symptoms]

print(user_symptoms)
predicted_disease = predict(user_symptoms)
print(predicted_disease)

# class ModelName:
#     def __init__(self):
#         self.variable = 1
        
#     # add models and other helper function

#     def analyze(self, query):
#         return query
