import pandas as pd

def read_file(train_file,test_file):
    training = pd.read_csv(train_file)
    testing = pd.read_csv(test_file)

read_file('Training.csv',"Testing.csv")


class ModelName:
    def __init__(self):
        self.variable = 1
        
    # add models and other helper function

    def analyze(self, query):
        return query
