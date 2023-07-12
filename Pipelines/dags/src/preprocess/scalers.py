"""
This module contains all the necessary functions to scale the  values to the data sets.
"""

import pandas as pd
import os
import pickle
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


current_dir = os.path.dirname(os.path.abspath(__file__))


# Ordinal


# Ordinal scaler
def fit_ordinal_scaler(ti):

    X_train_ordinal_imputed_path = ti.xcom_pull(task_ids="X_train_ordinal_impute", key="X_train_ordinal_imputed_path")

    X_train_ordinal_imputed_df = pd.read_csv(X_train_ordinal_imputed_path)

    scaler = MinMaxScaler()
    scaler.fit(X_train_ordinal_imputed_df)

    ordinal_scaler_path = os.path.join(current_dir, "../../models/scalers/ordinal_scaler.pkl")

    with open(ordinal_scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

    ti.xcom_push(key="ordinal_scaler_path", value=ordinal_scaler_path)

# Transform train
def transform_ordinal_train(ti):
    ordinal_scaler_path = ti.xcom_pull(task_ids="fit_ordinal_scaler", key="ordinal_scaler_path")

    with open(ordinal_scaler_path, 'rb') as f:
        ordinal_scaler = pickle.load(f)

    X_train_ordinal_imputed_path = ti.xcom_pull(task_ids="X_train_ordinal_impute", key="X_train_ordinal_imputed_path")

    X_train_ordinal_imputed_df = pd.read_csv(X_train_ordinal_imputed_path)

    X_train_ordinal_transformed = ordinal_scaler.transform(X_train_ordinal_imputed_df)

    X_train_ordinal_transformed_df = pd.DataFrame(X_train_ordinal_transformed, columns=X_train_ordinal_imputed_df.columns)

    X_train_ordinal_transformed_path = os.path.join(current_dir, '../../data/interim/X_train_ordinal_transformed.csv')
    X_train_ordinal_transformed_df.to_csv(X_train_ordinal_transformed_path, index=False, header=True)

    ti.xcom_push(key="X_train_ordinal_transformed_path", value=X_train_ordinal_transformed_path)

# Transform test
def transform_ordinal_test(ti):
    ordinal_scaler_path = ti.xcom_pull(task_ids="fit_ordinal_scaler", key="ordinal_scaler_path")

    with open(ordinal_scaler_path, 'rb') as f:
        ordinal_scaler = pickle.load(f)

    X_test_ordinal_imputed_path = ti.xcom_pull(task_ids="X_test_ordinal_impute", key="X_test_ordinal_imputed_path")

    X_test_ordinal_imputed_df = pd.read_csv(X_test_ordinal_imputed_path)

    X_test_ordinal_transformed = ordinal_scaler.transform(X_test_ordinal_imputed_df)

    X_test_ordinal_transformed_df = pd.DataFrame(X_test_ordinal_transformed, columns=X_test_ordinal_imputed_df.columns)

    X_test_ordinal_transformed_path = os.path.join(current_dir, '../../data/interim/X_test_ordinal_transformed.csv')
    X_test_ordinal_transformed_df.to_csv(X_test_ordinal_transformed_path, index=False, header=True)

    ti.xcom_push(key="X_test_ordinal_transformed_path", value=X_test_ordinal_transformed_path)


# Numerical scaler

# Function to fit the numerical scaler
def fit_numerical_scaler(ti):
    X_train_numerical_imputed_path = ti.xcom_pull(task_ids="X_train_numerical_impute", key="X_train_numerical_imputed_path")
    X_train_numerical_imputed_df = pd.read_csv(X_train_numerical_imputed_path)
    scaler = MinMaxScaler()
    scaler.fit(X_train_numerical_imputed_df)
    numerical_scaler_path = os.path.join(current_dir, "../../models/scalers/numerical_scaler.pkl")
    with open(numerical_scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    ti.xcom_push(key="numerical_scaler_path", value=numerical_scaler_path)

# Function to transform numerical train data
def transform_numerical_train(ti):
    numerical_scaler_path = ti.xcom_pull(task_ids="fit_numerical_scaler", key="numerical_scaler_path")
    with open(numerical_scaler_path, 'rb') as f:
        numerical_scaler = pickle.load(f)
    X_train_numerical_imputed_path = ti.xcom_pull(task_ids="X_train_numerical_impute", key="X_train_numerical_imputed_path")
    X_train_numerical_imputed_df = pd.read_csv(X_train_numerical_imputed_path)
    X_train_numerical_transformed = numerical_scaler.transform(X_train_numerical_imputed_df)
    X_train_numerical_transformed_df = pd.DataFrame(X_train_numerical_transformed, columns=X_train_numerical_imputed_df.columns)
    X_train_numerical_transformed_path = os.path.join(current_dir, '../../data/interim/X_train_numerical_transformed.csv')
    X_train_numerical_transformed_df.to_csv(X_train_numerical_transformed_path, index=False, header=True)
    ti.xcom_push(key="X_train_numerical_transformed_path", value=X_train_numerical_transformed_path)

# Function to transform numerical test data
def transform_numerical_test(ti):
    numerical_scaler_path = ti.xcom_pull(task_ids="fit_numerical_scaler", key="numerical_scaler_path")
    with open(numerical_scaler_path, 'rb') as f:
        numerical_scaler = pickle.load(f)
    X_test_numerical_imputed_path = ti.xcom_pull(task_ids="X_test_numerical_impute", key="X_test_numerical_imputed_path")
    X_test_numerical_imputed_df = pd.read_csv(X_test_numerical_imputed_path)
    X_test_numerical_transformed = numerical_scaler.transform(X_test_numerical_imputed_df)
    X_test_numerical_transformed_df = pd.DataFrame(X_test_numerical_transformed, columns=X_test_numerical_imputed_df.columns)
    X_test_numerical_transformed_path = os.path.join(current_dir, '../../data/interim/X_test_numerical_transformed.csv')
    X_test_numerical_transformed_df.to_csv(X_test_numerical_transformed_path, index=False, header=True)
    ti.xcom_push(key="X_test_numerical_transformed_path", value=X_test_numerical_transformed_path)


# Categorical

# Function to fit the categorical encoder
def fit_categorical_encoder(ti):
    X_train_categorical_imputed_path = ti.xcom_pull(task_ids="X_train_categorical_impute", key="X_train_categorical_imputed_path")
    X_train_categorical_imputed_df = pd.read_csv(X_train_categorical_imputed_path)
    encoder = OneHotEncoder(handle_unknown="ignore")
    encoder.fit(X_train_categorical_imputed_df)
    categorical_encoder_path = os.path.join(current_dir, "../../models/encoders/categorical_encoder.pkl")
    with open(categorical_encoder_path, 'wb') as f:
        pickle.dump(encoder, f)
    ti.xcom_push(key="categorical_encoder_path", value=categorical_encoder_path)

# Function to transform categorical train data
def transform_categorical_train(ti):
    categorical_encoder_path = ti.xcom_pull(task_ids="fit_categorical_encoder", key="categorical_encoder_path")
    with open(categorical_encoder_path, 'rb') as f:
        categorical_encoder = pickle.load(f)
    X_train_categorical_imputed_path = ti.xcom_pull(task_ids="X_train_categorical_impute", key="X_train_categorical_imputed_path")
    X_train_categorical_imputed_df = pd.read_csv(X_train_categorical_imputed_path)
    X_train_categorical_transformed = categorical_encoder.transform(X_train_categorical_imputed_df).toarray()
    X_train_categorical_transformed_df = pd.DataFrame(X_train_categorical_transformed, columns=categorical_encoder.get_feature_names_out())
    X_train_categorical_transformed_path = os.path.join(current_dir, '../../data/interim/X_train_categorical_transformed.csv')
    X_train_categorical_transformed_df.to_csv(X_train_categorical_transformed_path, index=False, header=True)
    ti.xcom_push(key="X_train_categorical_transformed_path", value=X_train_categorical_transformed_path)

# Function to transform categorical test data
def transform_categorical_test(ti):
    categorical_encoder_path = ti.xcom_pull(task_ids="fit_categorical_encoder", key="categorical_encoder_path")
    with open(categorical_encoder_path, 'rb') as f:
        categorical_encoder = pickle.load(f)
    X_test_categorical_imputed_path = ti.xcom_pull(task_ids="X_test_categorical_impute", key="X_test_categorical_imputed_path")
    X_test_categorical_imputed_df = pd.read_csv(X_test_categorical_imputed_path)
    X_test_categorical_transformed = categorical_encoder.transform(X_test_categorical_imputed_df).toarray()
    X_test_categorical_transformed_df = pd.DataFrame(X_test_categorical_transformed, columns=categorical_encoder.get_feature_names_out())
    X_test_categorical_transformed_path = os.path.join(current_dir, '../../data/interim/X_test_categorical_transformed.csv')
    X_test_categorical_transformed_df.to_csv(X_test_categorical_transformed_path, index=False, header=True)
    ti.xcom_push(key="X_test_categorical_transformed_path", value=X_test_categorical_transformed_path)
