"""
This script performs the necessary splitting of X_train and X_test for preprocessing
"""

# Dependencies

import os
import pandas as pd

numerical = ["age", "TSH", "T3", "TT4", "T4U", "FTI",
             ]

categorical = ["sex", "referral_source",
               ]

ordinal = ["FTI_measured", "T4U_measured", "TT4_measured", "T3_measured", "TSH_measured",
           "psych","hypopituitary", "tumor", "goitre", "lithium", "query_hyperthyroid", 
           "query_hypothyroid", "I131_treatment", "thyroid_surgery","pregnant",
           "sick", "on_antithyroid_medication", "query_on_thyroxine", "on_thyroxine",
           ]


current_dir = os.path.dirname(os.path.abspath(__file__))


def split_X_train(ti):
    X_train_path = ti.xcom_pull(task_ids='split_dataframe', key='X_train_path')
    df = pd.read_csv(X_train_path)

    train_ordinal = df[ordinal]
    train_numerical = df[numerical]
    train_categorical = df[categorical]

    train_ordinal_path = os.path.join(current_dir, '../../data/interim/train_ordinal.csv')
    train_numerical_path = os.path.join(current_dir, '../../data/interim/train_numerical.csv')
    train_categorical_path = os.path.join(current_dir, '../../data/interim/train_categorical.csv')

    train_ordinal.to_csv(train_ordinal_path, index=False)
    train_numerical.to_csv(train_numerical_path, index=False)
    train_categorical.to_csv(train_categorical_path, index=False)

    ti.xcom_push(key="train_ordinal_path", value=train_ordinal_path)
    ti.xcom_push(key="train_numerical_path", value=train_numerical_path)
    ti.xcom_push(key="train_categorical_path", value=train_categorical_path)


def split_X_test(ti):
    X_test_path = ti.xcom_pull(task_ids='split_dataframe', key='X_test_path')
    df = pd.read_csv(X_test_path)

    test_ordinal = df[ordinal]
    test_numerical = df[numerical]
    test_categorical = df[categorical]

    test_ordinal_path = os.path.join(current_dir, '../../data/interim/test_ordinal.csv')
    test_numerical_path = os.path.join(current_dir, '../../data/interim/test_numerical.csv')
    test_categorical_path = os.path.join(current_dir, '../../data/interim/test_categorical.csv')

    test_ordinal.to_csv(test_ordinal_path, index=False)
    test_numerical.to_csv(test_numerical_path, index=False)
    test_categorical.to_csv(test_categorical_path, index=False)

    ti.xcom_push(key="test_ordinal_path", value=test_ordinal_path)
    ti.xcom_push(key="test_numerical_path", value=test_numerical_path)
    ti.xcom_push(key="test_categorical_path", value=test_categorical_path)
