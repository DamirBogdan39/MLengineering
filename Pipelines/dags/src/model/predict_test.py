"""
This module contains the function that will use the trained xgboost model,
predict on test data and save a classification report.
"""

import pandas as pd
import os
import pickle
from sklearn.metrics import classification_report

current_dir = os.path.dirname(os.path.abspath(__file__))

def predict_test(ti):
    
    X_test_path = ti.xcom_pull(task_ids="merge_X_test_processed", key="X_test_processed_df_path")
    y_test_path = ti.xcom_pull(task_ids="encode_y_test", key="y_test_path")
    model_path = ti.xcom_pull(task_ids="fit_xgboost", key="model_path")

    X_test = pd.read_csv(X_test_path)
    y_test = pd.read_csv(y_test_path)

    with open(model_path, "rb") as file:
        xgboost_model = pickle.load(file)

    # Make predictions on the X_test data
    y_pred = xgboost_model.predict(X_test)

    # Generate a classification report
    classification_rep = classification_report(y_test, y_pred)

    # Define the path for saving the classification report
    report_path = os.path.join(current_dir, "../../reports/classification_report.txt")

    # Save the classification report in a file
    with open(report_path, "w") as file:
        file.write(classification_rep)