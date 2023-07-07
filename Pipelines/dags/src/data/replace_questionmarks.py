"""
This script replaces "?" values in the dataframe with np.nan
"""

# Dependencies
import numpy as np

# Function
def replace_questionmarks(ti):
    # Retrieve the output from t1 using xcom_pull
    df = ti.xcom_pull(task_ids='import_data')
    
    # Replace "?" with np.nan
    df.replace("?", np.nan, inplace=True)
    
    # Return the updated dataframe
    return df
