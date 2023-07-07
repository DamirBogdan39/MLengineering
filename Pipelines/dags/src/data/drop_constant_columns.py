"""
This script removes the "TBG" and "TBG_measured" columns from the dataframe
"""

# Dependencies
import pandas as pd


# Function
def drop_constant_columns(ti):
    # Retrieve the output from t2 using xcom_pull
    df = ti.xcom_pull(task_ids='replace_questionmarks')
    
    # Remove "TBG" and "TBG_measured" columns
    df.drop(["TBG", "TBG_measured"], axis=1, inplace=True)
    
    # Return the updated dataframe
    return df
