"""
Testing
"""

# Necessary imports
import joblib
import pandas as pd
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load df_test from the saved CSV file
df_test = pd.read_csv('../../data/data_1/df_test.csv')

# Split df_test into X_test and y_test
X_test = df_test.drop('diagnosis', axis=1)
y_test = df_test['diagnosis']

# Load the saved model as 'clf'
clf = joblib.load('../../models/model_1')

# Calculate the accuracy score of the decision tree classifier on the test data
y_pred = clf.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Write to file
with open('../../metrics/metrics_1.json', 'w') as outfile:
    json.dump({"accuracy":accuracy,
               "precision":precision,
               "recall":recall,
               "f1":f1}, outfile)
