import os
import subprocess
import pickle
import pandas as pd


class ChurnModel(object):

    def __init__(self):
        os.makedirs('model/')

        subprocess.run(['aws', 's3', 'cp', 's3://manticore-model-repository/churn', 'model/', '--recursive'])

        self.model = pickle.load(open("model/model", "rb"))

    def predict(self, X, features_names):

        # columns = ['Unnamed: 0', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
        #            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        #            'StreamingTV', 'StreamingMovies', 'PaperlessBilling',
        #            'MultipleLines_No', 'MultipleLines_No phone service',
        #            'MultipleLines_Yes', 'InternetService_DSL',
        #            'InternetService_Fiber optic', 'InternetService_No',
        #            'Contract_Month-to-month', 'Contract_One year', 'Contract_Two year',
        #            'PaymentMethod_Bank transfer (automatic)',
        #            'PaymentMethod_Credit card (automatic)',
        #            'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check',
        #            'tenure_group_Tenure_0-12', 'tenure_group_Tenure_12-24',
        #            'tenure_group_Tenure_24-48', 'tenure_group_Tenure_48-60',
        #            'tenure_group_Tenure_gt_60', 'tenure', 'MonthlyCharges',
        #            'TotalCharges']

        #df = pd.DataFrame(X.reshape(-1, X.shape[1]), columns=columns)

        #return self.model.predict(df)
        return self.model.predict(X)

