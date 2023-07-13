"""
This module contains all necessary functions to merge all features back into X_train and X_test data sets.
"""

import os
import pandas as pd
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))


def merge_X_train_processed(ti):

    ordinal_path = ti.xcom_pull(task_ids="transform_ordinal_train", key="X_train_ordinal_transformed_path")
    numerical_path = ti.xcom_pull(task_ids="transform_numerical_train", key="X_train_numerical_transformed_path")
    categorical_path = ti.xcom_pull(task_ids="transform_categorical_train", key="X_train_categorical_transformed_path")

    ordinal_df = pd.read_csv(ordinal_path)
    numerical_df = pd.read_csv(numerical_path)
    categorical_df = pd.read_csv(categorical_path)

    processed_df = pd.concat([ordinal_df, numerical_df, categorical_df], axis=1)

    processed_df_path = os.path.join(current_dir, "../../data/processed/X_train_processed.csv")

    processed_df.to_csv(processed_df_path, index=False)

    ti.xcom_push(key="X_train_processed_df_path", value=processed_df_path)


def merge_X_test_processed(ti):

    ordinal_path = ti.xcom_pull(task_ids="transform_ordinal_test", key="X_test_ordinal_transformed_path")
    numerical_path = ti.xcom_pull(task_ids="transform_numerical_test", key="X_test_numerical_transformed_path")
    categorical_path = ti.xcom_pull(task_ids="transform_categorical_test", key="X_test_categorical_transformed_path")

    ordinal_df = pd.read_csv(ordinal_path)
    numerical_df = pd.read_csv(numerical_path)
    categorical_df = pd.read_csv(categorical_path)

    processed_df = pd.concat([ordinal_df, numerical_df, categorical_df], axis=1)

    processed_df_path = os.path.join(current_dir, "../../data/processed/X_test_processed.csv")

    processed_df.to_csv(processed_df_path, index=False)

    ti.xcom_push(key="X_test_processed_df_path", value=processed_df_path)