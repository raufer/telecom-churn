import os
import pickle
import json
import argparse
import subprocess
import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.metrics import roc_auc_score, roc_curve, scorer
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score, recall_score


def main(args):
    os.makedirs('data/')
    os.makedirs('model/')
    os.makedirs('artifacts/')

    subprocess.run(['aws', 's3', 'cp', args.prepared_data_location, 'data/', '--recursive'])

    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("data/test.csv")

    subprocess.run(['cp', 'app/monthly_charges_distribution.png', 'artifacts/'])
    subprocess.run(['cp', 'app/payment_method_distribution.png', 'artifacts/'])

    for i in os.listdir('artifacts'):
        print(i)

    metadata = {
        'outputs': [
            {
              'storage': 'inline',
              'source': "## Customer Attrition\nCustomer attrition, also known as customer churn, customer turnover, or customer defection, is the loss of clients or customers.\n\nTelephone service companies, Internet service providers, pay TV companies, insurance firms, and alarm monitoring services, often use customer attrition analysis and customer attrition rates as one of their key business metrics because the cost of retaining an existing customer is far less than acquiring a new one.\n\nCompanies from these sectors often have customer service branches which attempt to win back defecting clients, because recovered long-term customers can be worth much more to a company than newly recruited clients.\n```\nRows     :  7043\nColumns  :  21\nFeatures : \n ['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn']\n ```",
              'type': 'markdown',
            }
        ]
    }
    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)

    for i in os.listdir('artifacts'):
        print(i)


if __name__ == "__main__":
    import os

    parser = argparse.ArgumentParser(description='Modeling for churn classification use case.')

    parser.add_argument('--prepared-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/prepared/')

    args = parser.parse_args()
    print(args)

    main(args)
