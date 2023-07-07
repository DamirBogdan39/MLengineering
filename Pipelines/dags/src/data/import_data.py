"""
This script imports the data into the pipeline
"""

# Dependencies
import os
import pandas as pd

# Import function
def import_data():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir, '../../data/raw/raw.csv')

    df = pd.read_csv(file_path)

    return df
