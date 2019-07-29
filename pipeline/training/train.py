import os
import pickle
import json
import argparse
import subprocess
import pandas as pd

from xgboost import XGBClassifier

from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
from sklearn.metrics import roc_auc_score,roc_curve,scorer
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score,recall_score




def main(args):

    os.makedirs('data/')
    subprocess.run(['aws', 's3', 'cp', args.prepared_data_location, 'data/', '--recursive'])

    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("data/test.csv")

    print("Train shape: {}".format(str(train.shape)))
    print("Test shape: {}".format(str(test.shape)))

    Id_col = ['customerID']
    target_col = ["Churn"]

    ##seperating dependent and independent variables
    cols = [i for i in train.columns if i not in Id_col + target_col]
    train_X = train[cols]
    train_Y = train[target_col]
    test_X = test[cols]
    test_Y = test[target_col]

    print("COLUMNS TRAIN PREPROCESSED: ", train_X.columns)
    print("COLUMNS TEST PREPROCESSED: ", test_X.columns)

    model = XGBClassifier(
        base_score=0.5,
        booster='gbtree',
        colsample_bylevel=1,
        colsample_bytree=1,
        gamma=0,
        learning_rate=0.9,
        max_delta_step=0,
        max_depth=7,
        min_child_weight=1,
        missing=None,
        n_estimators=100,
        n_jobs=1,
        nthread=None,
        objective='binary:logistic',
        random_state=0,
        reg_alpha=0,
        reg_lambda=1,
        scale_pos_weight=1,
        seed=None,
        silent=True,
        subsample=1
    )

    model.fit(train_X, train_Y)

    predictions = model.predict(test_X)
    probabilities = model.predict_proba(test_X)

    print("\n Classification report : \n", classification_report(test_Y, predictions))
    acc_score = accuracy_score(test_Y, predictions)
    print("Accuracy Score   : ", acc_score)
    # confusion matrix
    conf_matrix = confusion_matrix(test_Y, predictions)
    # roc_auc_score
    model_roc_auc = roc_auc_score(test_Y, predictions)
    print("Area under curve : ", model_roc_auc)
    fpr, tpr, thresholds = roc_curve(test_Y, probabilities[:, 1])

    metadata = {
        'data': {
            'prepared-data-location': args.prepared_data_location
        },
        'score': {
            'Area under curve': float(model_roc_auc),
            'Accuracy Score': float(acc_score)
        },
        'algorithm': 'XGBoost'
    }

    print("Saving model to: '{}'".format(args.model_repo_location))

    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=4)

    pickle.dump(model, open("model", "wb"))

    subprocess.run(['aws', 's3', 'cp', 'metadata.json', os.path.join(args.model_repo_location, 'metadata.json')])
    subprocess.run(['aws', 's3', 'cp', 'model', os.path.join(args.model_repo_location, 'model')])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Modeling for churn classification use case.')

    parser.add_argument('--prepared-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/prepared/')
    parser.add_argument('--model-repo-location', type=str, help='PLACEHOLDER', default='s3://manticore-model-repository/churn')

    args = parser.parse_args()
    print(args)

    main(args)
