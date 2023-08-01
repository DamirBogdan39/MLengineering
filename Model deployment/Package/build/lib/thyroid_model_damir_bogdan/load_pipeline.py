"""
This module contains the necessary function to import the working pipeline along with the necessary function definitions and utils.
"""

# Dependencies
import joblib
import numpy as np
from pathlib import Path

# Function definitions

# List of ordinal features in the data
ordinal = ['on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_medication',
           'sick', 'pregnant', 'thyroid_surgery', 'I131_treatment', 'query_hypothyroid',
           'query_hyperthyroid', 'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych',
           'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured', 'FTI_measured']

# Create a function to replace '?' with np.nan
def replace_question_mark(X):
    return X.replace('?', np.nan)

# Create a function to drop columns 'TBG' and 'TBG_measured'
def drop_columns(X):
    return X.drop(["TBG", "TBG_measured"], axis=1)  # Drop 'Class' column here

# Ordinal encoder function
def ordinal_encoder(X):
    # Convert ordinal features to categorical
    for col in ordinal:
        X[col] = X[col].astype("category")
    # Apply ordinal encoding to the ordinal features
    X_encoded = X[ordinal].apply(lambda x: x.cat.codes) 

    return X_encoded


# Load pipeline function
def load_pipeline():
    current_directory = Path(__file__).parent
    pipeline_path = current_directory / "pipeline.joblib"

    try:
        loaded_pipeline = joblib.load(pipeline_path)
        return loaded_pipeline
    except FileNotFoundError:
        return "Error: The 'pipeline.joblib' file does not exist."


