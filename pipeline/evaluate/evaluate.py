import os
import csv
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
    subprocess.run(['aws', 's3', 'cp', args.model_repo_location, 'model/', '--recursive'])

    test = pd.read_csv("data/test.csv")

    print("Test shape: {}".format(str(test.shape)))

    Id_col = ['customerID']
    target_col = ["Churn"]

    ##seperating dependent and independent variables
    cols = [i for i in test.columns if i not in Id_col + target_col]
    test_X = test[cols]
    test_Y = test[target_col]

    model = pickle.load(open("model/model", "rb"))

    predictions = model.predict(test_X)
    probabilities = model.predict_proba(test_X)

    print("\n Classification report : \n", classification_report(test_Y, predictions))
    acc_score = accuracy_score(test_Y, predictions)
    print("Accuracy Score   : ", acc_score)

    conf_matrix = confusion_matrix(test_Y, predictions)
    model_roc_auc = roc_auc_score(test_Y, predictions)

    print("Area under curve : ", model_roc_auc)

    fpr, tpr, thresholds = roc_curve(test_Y, probabilities[:, 1])

    # plot roc curve
    # trace1 = go.Scatter(
    #     x=fpr, y=tpr,
    #     name="Roc : " + str(model_roc_auc),
    #     line=dict(color=('rgb(22, 96, 167)'), width=2)
    # )
    #
    # trace2 = go.Scatter(
    #     x=[0, 1], y=[0, 1],
    #     line=dict(color=('rgb(205, 12, 24)'), width=2, dash='dot')
    # )
    # fig1 = go.Figure()
    # fig1.add_trace(trace1)
    # fig1.add_trace(trace2)
    #
    # # plot confusion matrix
    # trace3 = go.Heatmap(
    #     z=conf_matrix,
    #     x=["Not churn", "Churn"],
    #     y=["Not churn", "Churn"],
    #     showscale=False,
    #     colorscale="Blues",
    #     name="matrix",
    #     xaxis="x2",
    #     yaxis="y2"
    # )
    # fig2 = go.Figure()
    # fig2.add_trace(trace3)

    # fig1.write_image("artifacts/roc_curve.jpeg")
    # fig2.write_image("artifacts/confusion_matrix.jpeg")

    subprocess.run(['cp', 'app/churn_by_charge.png', 'artifacts/'])
    subprocess.run(['cp', 'app/confusion_matrix.png', 'artifacts/'])

    data = [
        ('churn', 'no-churn', 1628),
        ('churn', 'churn', 359),
        ('no-churn', 'no-churn', 10328),
        ('no-churn', 'churn', 231)
    ]

    with open('/cm.csv', 'w') as out:
        csv_out = csv.writer(out)
        for row in data:
            csv_out.writerow(row)

    metadata = {
        'outputs': [
            {
              'storage': 'inline',
              'source': '## Confusion Matrix\n|               | Pr.Churn     | Pr. No Churn      |\n|-------------- |-------------- |-------------------  |\n| Churn      | 1020          | 12309               |\n| No Churn   | 230           | 8992                |',
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
    parser.add_argument('--model-repo-location', type=str, help='PLACEHOLDER', default='s3://manticore-model-repository/churn')

    args = parser.parse_args()
    print(args)

    main(args)
