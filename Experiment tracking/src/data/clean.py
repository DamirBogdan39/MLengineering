"""
Cleaning the data
"""

# Imports

import pandas as pd
import numpy as np

# Read the data

df = pd.read_csv('../../data/raw/raw.csv')

# Replace ? with np.nan

df.replace('?', np.nan, inplace=True)

# Drop useless features

df.drop('TBG', axis=1, inplace=True)

df.drop('TBG_measured', axis=1, inplace=True)

# Recode numerical cols

numerical_columns = ['age','TSH', 'T3', 'TT4', 'T4U', 'FTI']
for col in numerical_columns:
  df[col] = df[col].astype('float64')

# Replacting max value of age

df['age'].replace(df['age'].max(), np.nan, inplace=True)

ordinal_features = ['on_thyroxine', 'query_on_thyroxine',
       'on_antithyroid_medication', 'sick', 'pregnant', 'thyroid_surgery',
       'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 'lithium',
       'goitre', 'tumor', 'hypopituitary', 'psych','TSH_measured', 'T3_measured',
       'TT4_measured','T4U_measured', 'FTI_measured']

for col in ordinal_features:
  df[col] = df[col].astype('category')

df[ordinal_features] = df[ordinal_features].apply(lambda x: x.cat.codes)

df.to_csv('../../data/interim/clean_df.csv', index=False)