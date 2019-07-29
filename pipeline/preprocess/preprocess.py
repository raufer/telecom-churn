import os
import argparse
import subprocess

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def data_preprocessing(telcom):
    # Data Preprocessing

    # customer id col
    Id_col = ['customerID']
    # Target columns
    target_col = ["Churn"]
    # categorical columns
    cat_cols = telcom.nunique()[telcom.nunique() < 6].keys().tolist()
    cat_cols = [x for x in cat_cols if x not in target_col]
    # numerical columns
    num_cols = [x for x in telcom.columns if x not in cat_cols + target_col + Id_col]
    # Binary columns with 2 values
    bin_cols = telcom.nunique()[telcom.nunique() == 2].keys().tolist()
    # Columns more than 2 values
    multi_cols = [i for i in cat_cols if i not in bin_cols]

    # Label encoding Binary columns
    le = LabelEncoder()
    for i in bin_cols:
        telcom[i] = le.fit_transform(telcom[i])

    # Duplicating columns for multi value columns
    telcom = pd.get_dummies(data=telcom, columns=multi_cols)

    # Scaling Numerical columns
    std = StandardScaler()
    telcom['TotalCharges'] = pd.to_numeric(telcom['TotalCharges'], errors='coerce')
    scaled = std.fit_transform(telcom[num_cols])
    scaled = pd.DataFrame(scaled, columns=num_cols)

    # dropping original values merging scaled values for numerical columns
    df_telcom_og = telcom.copy()
    telcom = telcom.drop(columns=num_cols, axis=1)
    telcom = telcom.merge(scaled, left_index=True, right_index=True, how="left")


    return telcom, df_telcom_og


# Tenure to categorical column
def tenure_lab(telcom):
    if telcom["tenure"] <= 12:
        return "Tenure_0-12"
    elif (telcom["tenure"] > 12) & (telcom["tenure"] <= 24):
        return "Tenure_12-24"
    elif (telcom["tenure"] > 24) & (telcom["tenure"] <= 48):
        return "Tenure_24-48"
    elif (telcom["tenure"] > 48) & (telcom["tenure"] <= 60):
        return "Tenure_48-60"
    elif telcom["tenure"] > 60:
        return "Tenure_gt_60"


def main(args):

    subprocess.run(['aws', 's3', 'cp', args.raw_data_location, 'data/', '--recursive'])

    telcom = pd.read_csv('data/churn_data.csv')

    print(telcom.head())
    print("Rows     : ", telcom.shape[0])
    print("Columns  : ", telcom.shape[1])
    print("\nFeatures : \n", telcom.columns.tolist())
    print("\nMissing values :  ", telcom.isnull().sum().values.sum())
    print("\nUnique values :  \n", telcom.nunique())

    telcom_pp, df_telcom_og = data_preprocessing(telcom)
    print(telcom_pp.head())

    # splitting train and test data
    train, test = train_test_split(telcom_pp, test_size=.25, random_state=111)

    os.makedirs('data/prepared/', exist_ok=True)

    train.to_csv('data/prepared/train.csv')
    test.to_csv('data/prepared/test.csv')


    subprocess.run(['aws', 's3', 'cp', 'data/prepared/', args.prepared_data_location, '--recursive'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/raw')
    parser.add_argument('--prepared-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/prepared/')

    args = parser.parse_args()
    print(args)

    main(args)


