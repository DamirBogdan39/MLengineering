'''
Data preparation and splitting
'''

#  Necessary imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# Importing the data
df = pd.read_csv('./data/iris.csv')


#  Dropping the id column
df.drop(['Id'], axis=1, inplace=True)


#  Creating a helper function to recode the target variable
def species_to_numeric(x):
    if x == 'Iris-setosa':
        return 0
    if x == 'Iris-versicolor':
        return 1
    if x == 'Iris-virginica':
        return 2


#  Transforming the target variable into numerical
df['Species'] = df['Species'].apply(species_to_numeric)


#  Splitting the features and target
X = df.drop(['Species'],axis=1).values
y = df['Species'].values


#  Train test split
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.5,
                                                    random_state=42)

# Define variable names
var_names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Target']


# Create train DataFrame and write it in data folder
data_train = np.column_stack((X_train, y_train))
train_df = pd.DataFrame(data_train, columns=var_names[:X_train.shape[1]] + [var_names[-1]])
train_df.to_csv('data/train_df.csv', index=False)

# Create test DataFrame
data_test = np.column_stack((X_test, y_test))
test_df = pd.DataFrame(data_test, columns=var_names[:X_test.shape[1]] + [var_names[-1]])
test_df.to_csv('data/test_df.csv', index=False)

