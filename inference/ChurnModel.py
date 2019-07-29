import os
import subprocess
import pickle


class ChurnModel(object):

    def __init__(self):
        os.makedirs('model/')

        subprocess.run(['aws', 's3', 'cp', 's3://manticore-model-repository/churn', 'model/', '--recursive'])

        self.model = pickle.load(open("model/model", "rb"))
        self.model._make_predict_function()

    def predict(self, X, features_names):
        return self.model.predict(X, batch_size=100, verbose=1)

