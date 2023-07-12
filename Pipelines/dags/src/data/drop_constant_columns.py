"""
This script removes the "TBG" and "TBG_measured" columns from the dataframe
"""

# Dependencies
import pandas as pd
import os

# Function

def drop_constant_columns(ti):

    # Retrieve the output from t2 using xcom_pull
    file_path = ti.xcom_pull(task_ids="replace_questionmarks", key="file_path")

    df = pd.read_csv(file_path)

    # Remove "TBG" and "TBG_measured" columns
    df.drop(["TBG", "TBG_measured"], axis=1, inplace=True)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, '../../data/interim/dropped_constant_cols.csv')
    
    df.to_csv(file_path, index=False)

    ti.xcom_push(key="file_path", value=file_path)