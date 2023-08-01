"""
A script that creates all necessary artifacts for packaging.
"""


# Dependencies

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib


categorical = ['sex', 'referral_source']

ordinal = ['on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_medication',
               'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid',
               'query_hyperthyroid', 'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych',
               'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured', 'FTI_measured']

numerical = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI']


# Create a function to replace '?' with np.nan
def replace_question_mark(X):
    return X.replace('?', np.nan)

# Create a function to drop columns 'A' and 'B'
def drop_columns(X):
    return X.drop(["TBG", "TBG_measured"], axis=1)  # Drop 'Class' column here

def ordinal_encoder(X):
    # Convert ordinal features to categorical
    for col in ordinal:
        X[col] = X[col].astype('category')
    # Apply ordinal encoding to the ordinal features
    X_encoded = X[ordinal].apply(lambda x: x.cat.codes)
    # Drop the original ordinal features and replace with encoded values
 
    return X_encoded

# Define the transformers for each data type

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])

ordinal_transformer = Pipeline(steps=[
    ('encoder', FunctionTransformer(ordinal_encoder)),
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])


# Combine all feature transformations using ColumnTransformer
preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_transformer, numerical),
    ('ord', ordinal_transformer, ordinal),
    ('cat', categorical_transformer, categorical),
])

# Create the final pipeline with replacing, dropping, encoding, and XGBoost classifier steps
pipeline = Pipeline(steps=[
    ('replace_question_mark', FunctionTransformer(replace_question_mark)),
    ('drop_columns', FunctionTransformer(drop_columns)),
    ('preprocessor', preprocessor),  # The preprocessor defined earlier
    ('xgb_classifier', XGBClassifier(n_estimators=100, max_depth=5, random_state=42))
])


df = pd.read_csv('raw.csv')

# Assuming 'df' is the DataFrame containing the data

# Define the features (X) and the target variable (y)
X = df.drop('Class', axis=1)
y = df['Class']

# Assuming 'y' is your target variable
label_encoder = LabelEncoder()
encoded_y = label_encoder.fit_transform(y)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, encoded_y, test_size=0.3, random_state=42, stratify=encoded_y)

pipeline.fit(X_train, y_train)

from sklearn.metrics import classification_report

# Save the pipeline and label_encoder
joblib.dump(pipeline, 'pipeline.joblib')
joblib.dump(label_encoder, 'label_encoder.joblib')

