"""
Cleaning
"""

# Necessary imports
import pandas as pd

# Importing the data
df = pd.read_csv('./data/data.csv')

# Remove 'id' column
df = df.drop('id', axis=1)

# Change values in 'diagnosis' column to 1 for 'M' and 0 for 'B'
df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

# Save the data
df.to_csv('data/df_clean.csv', index=False)