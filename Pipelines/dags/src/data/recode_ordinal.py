"""
This script recodes the ordinal features of the data set and returns only them.
"""

# Dependencies

import pandas as pd
import os

# Function

def recode_ordinal(ti):

    # Retrieve the output from task using xcom_pull

    file_path = ti.xcom_pull(task_ids='drop_constant_columns', key='file_path')
    
    df = pd.read_csv(file_path)
    
    # Recode ordinal cols

    ordinal_features = ['on_thyroxine', 'query_on_thyroxine',
       'on_antithyroid_medication', 'sick', 'pregnant', 'thyroid_surgery',
       'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 'lithium',
       'goitre', 'tumor', 'hypopituitary', 'psych','TSH_measured', 'T3_measured',
       'TT4_measured','T4U_measured', 'FTI_measured']

    for col in ordinal_features:
        df[col] = df[col].astype('category')

    df[ordinal_features] = df[ordinal_features].apply(lambda x: x.cat.codes)

    # Return only the ordinal featues
    
    df_ord = df[ordinal_features]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path_ord = os.path.join(current_dir, '../../data/interim/ord_cols.csv')
    
    df_ord.to_csv(file_path_ord, index=False)

    ti.xcom_push(key="file_path_ord", value=file_path_ord)
    