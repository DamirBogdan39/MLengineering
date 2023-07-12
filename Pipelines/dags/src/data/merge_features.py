"""
This script replaces the original columns with the recoded columns.
"""
# Dependencies
import pandas as pd
import os

# Function

def merge_features(ti):
    # Retrieve the outputs from the previous tasks using xcom_pull
    
    path_to_df = ti.xcom_pull(task_ids="drop_constant_columns", key="file_path")
    path_num = ti.xcom_pull(task_ids="clean_age_feature", key="file_path_age")
    path_ord = ti.xcom_pull(task_ids='recode_ordinal_features', key="file_path_ord")

    df = pd.read_csv(path_to_df)
    df_num = pd.read_csv(path_num)
    df_ord = pd.read_csv(path_ord)

    # Replace columns in df with values from df1 and df2 if they exist
    for column in df.columns:
        if column in df_num.columns:
            df[column] = df_num[column]
        if column in df_ord.columns:
            df[column] = df_ord[column]

    # Return the modified dataframe
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path_cleaned = os.path.join(current_dir, '../../data/interim/merged_cleaned.csv')
    
    df.to_csv(file_path_cleaned, index=False)

    ti.xcom_push(key="file_path", value=file_path_cleaned)
