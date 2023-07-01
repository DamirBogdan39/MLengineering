"""
Preprocessing of the data
"""

# Importing packages

import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn_pandas import DataFrameMapper, gen_features


df = pd.read_csv('../../data/interim/hyperparams_clean_df.csv')

# Splitting into features and target

X = df.drop('Class', axis=1)
y = df['Class']

# Creating a train and test split

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.3,
                                                    stratify=y,
                                                    random_state=42)

# Imputing missing values

categorical = df.select_dtypes(include=['object']).columns.tolist()
categorical.remove('Class')
ordinal = df.select_dtypes(include=['category']).columns.tolist()
numerical = df.select_dtypes(exclude=['category', 'object']).columns.tolist()

# Numerical

numerical_def = gen_features(
    columns=[[c] for c in numerical],
    classes=[
        {'class': SimpleImputer, 'strategy': 'median'},
        {'class': MinMaxScaler}
    ]
)

# Ordinal

ordinal_def = gen_features(
    columns=[[c] for c in ordinal],
    classes=[
        {'class': SimpleImputer, 'strategy': 'most_frequent'}
    ]
)

# Categorical

categorical_def = gen_features(
    columns=[[c] for c in categorical],
    classes=[
        {'class': SimpleImputer, 'strategy': 'constant', 'fill_value': 'missing'},
        {'class': OneHotEncoder, 'handle_unknown': 'ignore'}
    ]
)

features = numerical_def + categorical_def + ordinal_def
mapper = DataFrameMapper(features)

# Transforming the variables
X_train_tr = pd.DataFrame(mapper.fit_transform(X_train))
X_test_tr = pd.DataFrame(mapper.transform(X_test))

# Rename the features

column_names = list(mapper.transformed_names_) + ['target']

data_train = np.column_stack((X_train_tr, y_train))

df_train = pd.DataFrame(data_train, columns=column_names)
data_test = np.column_stack((X_test_tr, y_test))

df_test = pd.DataFrame(data_test, columns=column_names)

# Save the dataframes
df_train.to_csv('../../data/processed/hyperparams_train_df.csv', index=False)
df_test.to_csv('../../data/processed/hyperparams_test_df.csv', index=False)
