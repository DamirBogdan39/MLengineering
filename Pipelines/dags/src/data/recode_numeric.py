"""
This script recodes the numeric column into the right type and only returns them.
"""

# Dependencies

import pandas as pd
import os

# Function
def recode_numeric(ti):

    # Retrieve the output from task using xcom_pull

    file_path = ti.xcom_pull(task_ids='drop_constant_columns', key='file_path')
    
    # Recode numerical cols
    df = pd.read_csv(file_path)

    numerical_columns = ['age','TSH', 'T3', 'TT4', 'T4U', 'FTI']
    
    for col in numerical_columns:
        df[col] = df[col].astype('float64')

    # Return the dataframe with numeric cols

    df_num = df[numerical_columns]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path_num = os.path.join(current_dir, '../../data/interim/num_cols.csv')
    
    df_num.to_csv(file_path_num, index=False)

    ti.xcom_push(key="file_path_num", value=file_path_num)