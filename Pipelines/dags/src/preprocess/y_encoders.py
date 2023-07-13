"""
This module contains the funcions necessary to encode y_train and y_test classes.
"""

import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

current_dir = os.path.dirname(os.path.abspath(__file__))

def encode_y_train(ti):
    y_train_path = ti.xcom_pull(task_ids="split_dataframe", key="y_train_path")
    y_train = pd.read_csv(y_train_path)

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_train_encoded_df = pd.DataFrame(data=y_train_encoded, columns=["y_train_encoded"])

    y_train_encoded_path = os.path.join(current_dir, "../../data/processed/y_train_encoded.csv")
    y_train_encoded_df.to_csv(y_train_encoded_path, index=False)

    ti.xcom_push(key="y_train_path", value=y_train_encoded_path)


def encode_y_test(ti):
    y_test_path = ti.xcom_pull(task_ids="split_dataframe", key="y_test_path")
    y_test = pd.read_csv(y_test_path)

    label_encoder = LabelEncoder()
    y_test_encoded = label_encoder.fit_transform(y_test)
    y_test_encoded_df = pd.DataFrame(data=y_test_encoded, columns=["y_test_encoded"])

    y_test_encoded_path = os.path.join(current_dir, "../../data/processed/y_test_encoded.csv")
    y_test_encoded_df.to_csv(y_test_encoded_path, index=False)

    ti.xcom_push(key="y_test_path", value=y_test_encoded_path)
