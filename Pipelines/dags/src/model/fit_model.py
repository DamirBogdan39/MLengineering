"""
This module contains a function that will train the model on the X_train and y_train data,
and save the model for future predictions.
"""

import pandas as pd
import os
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))

def fit_xgboost(ti):

    X_train_path = ti.xcom_pull(task_ids="merge_X_train_processed", key="X_train_processed_df_path")
    y_train_path = ti.xcom_pull(task_ids="encode_y_train", key="y_train_path")

    X_train = pd.read_csv(X_train_path)
    y_train = pd.read_csv(y_train_path)

    # Define the parameter grid

    param_grid = {
        "max_depth": [3, 5, 7],
        "n_estimators": [100, 200, 300],
    }


    # Create an XGBoost classifier
    xgb_model = XGBClassifier()

    # Create a GridSearchCV object
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring="balanced_accuracy", cv=5, n_jobs=-1)

    # Perform grid search cross-validation
    grid_search.fit(X_train, y_train)  # X_train and y_train are your training data

    best_model = grid_search.best_estimator_

    model_path = os.path.join(current_dir, "../../models/xgboost_model.pkl")

    with open(model_path, "wb") as file:
        pickle.dump(best_model, file)

    ti.xcom_push(key="model_path", value=model_path)

