"""
Training
"""

#  Necessary imports
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

# Importint the data

df = pd.read_csv('data/train_df.csv')

dtc = DecisionTreeClassifier(random_state=42)

dtc.fit(df.drop('Target', axis=1), df['Target'])

# Save the trained model as 'model'
joblib.dump(dtc, 'model')