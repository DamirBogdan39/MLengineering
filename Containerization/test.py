"""
Testing
"""

# Necessary imports
import joblib
import pandas as pd
from sklearn.metrics import classification_report

# Load df_test from the saved CSV file
df_test = pd.read_csv('data/test_df.csv')

# Split df_test into X_test and y_test
X_test = df_test.drop('Target', axis=1)
y_test = df_test['Target']

# Load the saved model as 'clf'
dtc = joblib.load('model')

# Calculate the accuracy score of the decision tree classifier on the test data
y_pred = dtc.predict(X_test)

# Classification report

print(classification_report(y_test, y_pred))
