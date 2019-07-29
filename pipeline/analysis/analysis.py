import os
import pickle
import json
import argparse
import subprocess
import pandas as pd
import plotly


import plotly.offline as py  # visualization
import plotly.graph_objs as go  # visualization
import plotly.tools as tls  # visualization
import plotly.figure_factory as ff  # visualization

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


if __name__ == "__main__":
    import os

    parser = argparse.ArgumentParser(description='Modeling for churn classification use case.')

    parser.add_argument('--prepared-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/prepared/')

    args = parser.parse_args()
    print(args)

    main(args)
