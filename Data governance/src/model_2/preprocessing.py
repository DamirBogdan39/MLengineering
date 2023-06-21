"""
Preprocessing
"""

# Necessary imports
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Importing the data
df = pd.read_csv('../../data/data_2/df_clean.csv')

# Split dataframe into train and test sets
X = df.drop('diagnosis', axis=1)
y = df['diagnosis']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the columns in train and test sets
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create df_train by merging X_train and y_train with feature names preserved
feature_names = X.columns.tolist()
df_train = pd.DataFrame(X_train, columns=feature_names)
df_train['diagnosis'] = y_train.reset_index(drop=True)

# Create df_test by merging X_test and y_test with feature names preserved
df_test = pd.DataFrame(X_test, columns=feature_names)
df_test['diagnosis'] = y_test.reset_index(drop=True)


# Save the data into data folder
df_train.to_csv('../../data/data_2/df_train.csv', index=False)
df_test.to_csv('../../data/data_2/df_test.csv', index=False)