"""
This script replaces "?" values in the dataframe with np.nan
"""

# Dependencies
import numpy as np
import pandas as pd
import os

# Function
def replace_questionmarks(ti):

    # Retrieve the output from t1 using xcom_pull
    file_path = ti.xcom_pull(task_ids="import_and_merge_sources", key="file_path")

    df = pd.read_csv(file_path)

    # Replace "?" with np.nan
    df.replace("?", np.nan, inplace=True)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, '../../data/interim/removed_questionmarks.csv')
    
    df.to_csv(file_path, index=False)

    ti.xcom_push(key="file_path", value=file_path)
