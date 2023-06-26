"""
Training of the model
"""

# Importing packages

import joblib
import mlflow

import pandas as pd

from sklearn.ensemble import RandomForestClassifier

# Read the data

df = pd.read_csv('../../data/processed/train_df.csv')

# Get features and target

X_train = df.drop('target', axis=1)
y_train = df['target']

# Create classifier

clf = RandomForestClassifier(random_state=42)

# Fit the data

clf.fit(X_train, y_train)

joblib.dump(clf, '../../models/model')

print(df.target.value_counts())