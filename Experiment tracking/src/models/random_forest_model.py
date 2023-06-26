"""
This script contains the complete training and testing of a RandomForestClassifier model
"""

# Importing packages

import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score
import os

# Specify the URI

os.environ["MLFLOW_TRACKING_URI"] = "../../mlruns"

# Read the data

train_df = pd.read_csv('../../data/processed/train_df.csv')

test_df = pd.read_csv('../../data/processed/test_df.csv')

# Get features and target

X_train = train_df.drop('target', axis=1)
y_train = train_df['target']

X_test = test_df.drop('target', axis=1)
y_test = test_df['target']

# Create classifier

clf = RandomForestClassifier(random_state=42)

# Fit the data

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
recall_macro = recall_score(y_test, y_pred, average='macro')
f1_macro = f1_score(y_test, y_pred, average='macro')