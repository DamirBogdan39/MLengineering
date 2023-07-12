"""
This script imports the data into the pipeline.
"""

# Dependencies
import os
import pandas as pd

# Import function

def import_and_merge_sources(ti):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path_1 = os.path.join(current_dir, '../../data/raw/source_1.csv')
    
    # Import from first source

    df_source_1 = pd.read_csv(file_path_1)

    file_path_2 = os.path.join(current_dir, '../../data/raw/source_2.parquet')
    
    # Import from second source

    df_source_2 = pd.read_parquet(file_path_2)

    # Concatenate the DataFrames

    df = pd.concat([df_source_1, df_source_2], axis=1)

    # Return the merged DataFrame

    file_path = os.path.join(current_dir, '../../data/interim/merged.csv')

    df.to_csv(file_path, index=False)

    ti.xcom_push(key="file_path", value=file_path)