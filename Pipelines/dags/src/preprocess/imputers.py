"""
This module contains all the necessary functions to impute missing values to the data sets.
"""

# Dependencies
from sklearn.impute import SimpleImputer
import os
import pickle
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))

# Function to fit the ordinal imputer

def fit_ordinal_imputer(ti):
    
    X_train_ordinal_path = ti.xcom_pull(task_ids="split_X_train", key="train_ordinal_path")

    X_train_df= pd.read_csv(X_train_ordinal_path)
    
    imputer = SimpleImputer(strategy="most_frequent")

    imputer.fit(X_train_df)
    
    # Save imputer in task_instance
    
    imputer_path = os.path.join(current_dir, "../../models/imputers/ordinal_imputer.pkl")

    with open(imputer_path, 'wb') as f:
        pickle.dump(imputer, f)

    ti.xcom_push(key="imputer_path", value=imputer_path)

# Function to transform ordinal train data

def X_train_ordinal_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_ordinal_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_train_ordinal_path = ti.xcom_pull(task_ids="split_X_train", key="train_ordinal_path")
    
    X_train_ordinal_df = pd.read_csv(X_train_ordinal_path)
    
    X_train_ordinal_imputed = imputer.transform(X_train_ordinal_df)
    
    X_train_ordinal_imputed_df = pd.DataFrame(X_train_ordinal_imputed, columns=X_train_ordinal_df.columns)
    
    X_train_ordinal_imputed_path = os.path.join(current_dir, '../../data/interim/X_train_ordinal_imputed.csv')
    X_train_ordinal_imputed_df.to_csv(X_train_ordinal_imputed_path, index=False)
    
    ti.xcom_push(key="X_train_ordinal_imputed_path", value=X_train_ordinal_imputed_path)

# Function to transform ordinal test data

def X_test_ordinal_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_ordinal_imputer", key="imputer_path")

    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)

    X_test_ordinal_path = ti.xcom_pull(task_ids="split_X_test", key="test_ordinal_path")

    X_test_ordinal_df = pd.read_csv(X_test_ordinal_path)

    X_test_ordinal_imputed = imputer.transform(X_test_ordinal_df)

    X_test_ordinal_imputed_df = pd.DataFrame(X_test_ordinal_imputed, columns=X_test_ordinal_df.columns)

    X_test_ordinal_imputed_path = os.path.join(current_dir, '../../data/interim/X_test_ordinal_imputed.csv')
    X_test_ordinal_imputed_df.to_csv(X_test_ordinal_imputed_path, index=False)

    ti.xcom_push(key="X_test_ordinal_imputed_path", value=X_test_ordinal_imputed_path)

# Numerical imputer

# Function to fit the numerical imputer
def fit_numerical_imputer(ti):
    X_train_numerical_path = ti.xcom_pull(task_ids="split_X_train", key="train_numerical_path")
    X_train_df = pd.read_csv(X_train_numerical_path)
    
    imputer = SimpleImputer(strategy="median")
    imputer.fit(X_train_df)
    
    imputer_path = os.path.join(current_dir, "../../models/imputers/numerical_imputer.pkl")
    with open(imputer_path, 'wb') as f:
        pickle.dump(imputer, f)
    
    ti.xcom_push(key="imputer_path", value=imputer_path)

# Function to transform numerical train data
def X_train_numerical_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_numerical_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_train_numerical_path = ti.xcom_pull(task_ids="split_X_train", key="train_numerical_path")
    X_train_numerical_df = pd.read_csv(X_train_numerical_path)
    
    X_train_numerical_imputed = imputer.transform(X_train_numerical_df)
    X_train_numerical_imputed_df = pd.DataFrame(X_train_numerical_imputed, columns=X_train_numerical_df.columns)
    
    X_train_numerical_imputed_path = os.path.join(current_dir, '../../data/interim/X_train_numerical_imputed.csv')
    X_train_numerical_imputed_df.to_csv(X_train_numerical_imputed_path, index=False)
    
    ti.xcom_push(key="X_train_numerical_imputed_path", value=X_train_numerical_imputed_path)

# Function to transform numerical test data
def X_test_numerical_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_numerical_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_test_numerical_path = ti.xcom_pull(task_ids="split_X_test", key="test_numerical_path")
    X_test_numerical_df = pd.read_csv(X_test_numerical_path)
    
    X_test_numerical_imputed = imputer.transform(X_test_numerical_df)
    X_test_numerical_imputed_df = pd.DataFrame(X_test_numerical_imputed, columns=X_test_numerical_df.columns)
    
    X_test_numerical_imputed_path = os.path.join(current_dir, '../../data/interim/X_test_numerical_imputed.csv')
    X_test_numerical_imputed_df.to_csv(X_test_numerical_imputed_path, index=False)
    
    ti.xcom_push(key="X_test_numerical_imputed_path", value=X_test_numerical_imputed_path)

# Categorical

# Function to fit the categorical imputer
def fit_categorical_imputer(ti):
    X_train_categorical_path = ti.xcom_pull(task_ids="split_X_train", key="train_categorical_path")
    X_train_df = pd.read_csv(X_train_categorical_path)
    
    imputer = SimpleImputer(strategy="constant", fill_value='missing')
    imputer.fit(X_train_df)
    
    imputer_path = os.path.join(current_dir, "../../models/imputers/categorical_imputer.pkl")
    with open(imputer_path, 'wb') as f:
        pickle.dump(imputer, f)
    
    ti.xcom_push(key="imputer_path", value=imputer_path)

# Function to transform categorical train data
def X_train_categorical_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_categorical_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_train_categorical_path = ti.xcom_pull(task_ids="split_X_train", key="train_categorical_path")
    X_train_categorical_df = pd.read_csv(X_train_categorical_path)
    
    X_train_categorical_imputed = imputer.transform(X_train_categorical_df)
    X_train_categorical_imputed_df = pd.DataFrame(X_train_categorical_imputed, columns=X_train_categorical_df.columns)
    
    X_train_categorical_imputed_path = os.path.join(current_dir, '../../data/interim/X_train_categorical_imputed.csv')
    X_train_categorical_imputed_df.to_csv(X_train_categorical_imputed_path, index=False)
    
    ti.xcom_push(key="X_train_categorical_imputed_path", value=X_train_categorical_imputed_path)

# Function to transform categorical test data
def X_test_categorical_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_categorical_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_test_categorical_path = ti.xcom_pull(task_ids="split_X_test", key="test_categorical_path")
    X_test_categorical_df = pd.read_csv(X_test_categorical_path)
    
    X_test_categorical_imputed = imputer.transform(X_test_categorical_df)
    X_test_categorical_imputed_df = pd.DataFrame(X_test_categorical_imputed, columns=X_test_categorical_df.columns)
    
    X_test_categorical_imputed_path = os.path.join(current_dir, '../../data/interim/X_test_categorical_imputed.csv')
    X_test_categorical_imputed_df.to_csv(X_test_categorical_imputed_path, index=False)
    
    ti.xcom_push(key="X_test_categorical_imputed_path", value=X_test_categorical_imputed_path)
