"""
This script splits the dataframe into X_train, X_test, y_train and y_test
"""

from sklearn.model_selection import train_test_split
import pandas as pd
import os

# Function

def split_dataframe(ti):
    file_path = ti.xcom_pull(task_ids="merge_features", key='file_path')
    df = pd.read_csv(file_path)

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Save X_train
    X_train_path = os.path.join(current_dir, '../../data/interim/X_train.csv')
    X_train.to_csv(X_train_path, index=False)
    ti.xcom_push(key="X_train_path", value=X_train_path)

    # Save X_test
    X_test_path = os.path.join(current_dir, '../../data/interim/X_test.csv')
    X_test.to_csv(X_test_path, index=False)
    ti.xcom_push(key="X_test_path", value=X_test_path)

    # Save y_train
    y_train_path = os.path.join(current_dir, '../../data/interim/y_train.csv')
    y_train.to_csv(y_train_path, index=False)
    ti.xcom_push(key="y_train_path", value=y_train_path)

    # Save y_test
    y_test_path = os.path.join(current_dir, '../../data/interim/y_test.csv')
    y_test.to_csv(y_test_path, index=False)
    ti.xcom_push(key="y_test_path", value=y_test_path)



