"""
Training
"""

# Necessary imports
import pandas as pd
from sklearn.svm import LinearSVC
import joblib

# Load df_train from the saved CSV file
df_train = pd.read_csv('../../data/data_3/df_train.csv')

# Split df_train into X_train and y_train
X_train = df_train.drop('diagnosis', axis=1)
y_train = df_train['diagnosis']

# Train a decision tree classifier
clf = LinearSVC(random_state=42)
clf.fit(X_train, y_train)

# Save the trained model as 'model'
joblib.dump(clf, '../../models/model_3')