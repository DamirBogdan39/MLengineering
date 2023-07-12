"""
This script removes the unvalid value in the age feature of the dataframe.
"""

# Dependencies

import numpy as np
import os
import pandas as pd

def clean_age_feature(ti):
    
    # Retrieve the output from task using xcom_pull
    num_path = ti.xcom_pull(task_ids="recode_numeric_features", key="file_path_num")

    df = pd.read_csv(num_path)

    # Remove the unvalid age value.

    df['age'].replace(df['age'].max(), np.nan, inplace=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path_age = os.path.join(current_dir, '../../data/interim/num_cols_age_cleaned.csv')
    
    df.to_csv(file_path_age, index=False)

    ti.xcom_push(key="file_path_age", value=file_path_age)