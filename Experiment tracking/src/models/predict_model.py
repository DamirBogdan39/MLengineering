"""
Testing the metrics of the model on the test set
"""
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, balanced_accuracy_score, recall_score, f1_score
import mlflow

df = pd.read_csv('../../data/processed/test_df.csv')

X_test = df.drop('target', axis=1)
y_test = df['target']

clf = joblib.load('../../models/model')

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
recall_macro = recall_score(y_test, y_pred, average='macro')
f1_macro = f1_score(y_test, y_pred, average='macro')

print(accuracy, recall_macro, f1_macro)