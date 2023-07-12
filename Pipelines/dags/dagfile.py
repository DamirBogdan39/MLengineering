"""
A dagfile containing everything necessary o create a airflow DAG
"""

# Importing dependecies

import airflow

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import timedelta, datetime
import os
import pandas as pd

# Import the functions from the scripts

from src.data.import_data import import_and_merge_sources

from src.data.replace_questionmarks import replace_questionmarks
from src.data.drop_constant_columns import drop_constant_columns
from src.data.recode_numeric import recode_numeric
from src.data.recode_ordinal import recode_ordinal
from src.data.clean_age_feature import clean_age_feature
from src.data.merge_features import merge_features

from src.preprocess.split_dataframe import split_dataframe
from src.preprocess.split_X import *
from src.preprocess.imputers import *
from src.preprocess.scalers import *

# Default configuration arguments

default_args = {
    "owner": "aiflow",
    "start_date": airflow.utils.dates.days_ago(2),
    # "end_date": datetime(2023, 7, 15),
    "depends_on_past": False,
    "email": ['damirbogdan39@gmail.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retry": 1,
    "retry_delay": timedelta(minutes=5),
}


# Defining a DAG object

dag = DAG(
    "thyroid_preprocessing_DAG",
    default_args=default_args,
    description="DAG for preprocessing pipeline",
    schedule_interval=None,
    is_paused_upon_creation=True,
)


# Define the tasks

# Task 1 - merge the sources

import_merge_data_task = PythonOperator(
    task_id="import_and_merge_sources",
    python_callable=import_and_merge_sources,
    dag=dag,
)

# Task 2 - replace questionmarks

replace_questionmarks_task = PythonOperator(
    task_id="replace_questionmarks",
    python_callable=replace_questionmarks,
    dag=dag,
)

# Task 3 - drop constant features

drop_constant_columns_task = PythonOperator(
    task_id="drop_constant_columns",
    python_callable=drop_constant_columns,
    dag=dag,
)

# Task 4 - recode numerical features

recode_numeric_task = PythonOperator(
    task_id="recode_numeric_features",
    python_callable=recode_numeric,
    dag=dag,
)

# Task 5 - recode ordinal features 

recode_ordinal_task = PythonOperator(
    task_id="recode_ordinal_features",
    python_callable=recode_ordinal,
    dag=dag,
)

# Task 6 - clean age feature

clean_age_feature_task = PythonOperator(
    task_id="clean_age_feature",
    python_callable=clean_age_feature,
    dag=dag,
)

# Task 7 - merge are features into one dataframe

merge_features_task = PythonOperator(
    task_id="merge_features",
    python_callable=merge_features,
    dag=dag,
)

# Task 8 - perform a train test split

split_dataframe_task = PythonOperator(
    task_id="split_dataframe",
    python_callable=split_dataframe,
    dag=dag,
)

split_X_train_task= PythonOperator(
    task_id="split_X_train",
    python_callable=split_X_train,
    dag=dag,
)

split_X_test_task= PythonOperator(
    task_id="split_X_test",
    python_callable=split_X_test,
    dag=dag,
)

fit_ordinal_imputer_task = PythonOperator(
    task_id="fit_ordinal_imputer",
    python_callable=fit_ordinal_imputer,
    dag=dag,
)

X_train_ordinal_impute_task = PythonOperator(
    task_id="X_train_ordinal_impute",
    python_callable=X_train_ordinal_impute,
    dag=dag,
)

X_test_ordinal_impute_task = PythonOperator(
    task_id="X_test_ordinal_impute",
    python_callable=X_test_ordinal_impute,
    dag=dag,
)

fit_numerical_imputer_task = PythonOperator(
    task_id="fit_numerical_imputer",
    python_callable=fit_numerical_imputer,
    dag=dag,
)

X_train_numerical_impute_task = PythonOperator(
    task_id="X_train_numerical_impute",
    python_callable=X_train_numerical_impute,
    dag=dag,
)

X_test_numerical_impute_task = PythonOperator(
    task_id="X_test_numerical_impute",
    python_callable=X_test_numerical_impute,
    dag=dag,
)

fit_categorical_imputer_task = PythonOperator(
    task_id="fit_categorical_imputer",
    python_callable=fit_categorical_imputer,
    dag=dag,
)

X_train_categorical_impute_task = PythonOperator(
    task_id="X_train_categorical_impute",
    python_callable=X_train_categorical_impute,
    dag=dag,
)

X_test_categorical_impute_task = PythonOperator(
    task_id="X_test_categorical_impute",
    python_callable=X_test_categorical_impute,
    dag=dag,
)

fit_ordinal_scaler_task = PythonOperator(
    task_id="fit_ordinal_scaler",
    python_callable=fit_ordinal_scaler,
    dag=dag,
)

transform_ordinal_train_task = PythonOperator(
    task_id="transform_ordinal_train",
    python_callable=transform_ordinal_train,
    dag=dag,
)

transform_ordinal_test_task = PythonOperator(
    task_id="transform_ordinal_test",
    python_callable=transform_ordinal_test,
    dag=dag,
)

fit_numerical_scaler_task = PythonOperator(
    task_id="fit_numerical_scaler",
    python_callable=fit_numerical_scaler,
    dag=dag,
)

transform_numerical_train_task = PythonOperator(
    task_id="transform_numerical_train",
    python_callable=transform_numerical_train,
    dag=dag,
)

transform_numerical_test_task = PythonOperator(
    task_id="transform_numerical_test",
    python_callable=transform_numerical_test,
    dag=dag,
)

fit_categorical_encoder_task = PythonOperator(
    task_id="fit_categorical_encoder",
    python_callable=fit_categorical_encoder,
    dag=dag,
)

transform_categorical_train_task = PythonOperator(
    task_id="transform_categorical_train",
    python_callable=transform_categorical_train,
    dag=dag,
)

transform_categorical_test_task = PythonOperator(
    task_id="transform_categorical_test",
    python_callable=transform_categorical_test,
    dag=dag,
)



# DAG dependencies

# Cleaning
import_merge_data_task >> replace_questionmarks_task >> drop_constant_columns_task
drop_constant_columns_task >> [recode_numeric_task, recode_ordinal_task]
recode_numeric_task >> clean_age_feature_task
[drop_constant_columns_task, recode_ordinal_task, clean_age_feature_task] >> merge_features_task

# Preprocessing

#Imputers
merge_features_task >> split_dataframe_task
split_dataframe_task >> [split_X_train_task, split_X_test_task]
[split_X_train_task, split_X_test_task] >> fit_ordinal_imputer_task
fit_ordinal_imputer_task >> [X_train_ordinal_impute_task, X_test_ordinal_impute_task]
[split_X_train_task, split_X_test_task] >> fit_numerical_imputer_task
fit_numerical_imputer_task >> [X_train_numerical_impute_task, X_test_numerical_impute_task]
[split_X_train_task, split_X_test_task] >> fit_categorical_imputer_task
fit_categorical_imputer_task >> [X_train_categorical_impute_task, X_test_categorical_impute_task]

# Scalers
# Ordinal
[X_train_ordinal_impute_task, X_test_ordinal_impute_task] >> fit_ordinal_scaler_task
fit_ordinal_scaler_task >> [transform_ordinal_train_task, transform_ordinal_test_task]
[X_train_ordinal_impute_task, X_test_ordinal_impute_task] >> transform_ordinal_train_task
[X_train_ordinal_impute_task, X_test_ordinal_impute_task] >> transform_ordinal_test_task

# Numerical
[X_train_numerical_impute_task, X_test_numerical_impute_task] >> fit_numerical_scaler_task
fit_numerical_scaler_task >> [transform_numerical_train_task, transform_numerical_test_task]
[X_train_numerical_impute_task, X_test_numerical_impute_task] >> transform_numerical_train_task
[X_train_numerical_impute_task, X_test_numerical_impute_task] >> transform_numerical_test_task

# Categorical
[X_train_categorical_impute_task, X_test_categorical_impute_task] >> fit_categorical_encoder_task
fit_categorical_encoder_task >> [transform_categorical_train_task, transform_categorical_test_task]
[X_train_categorical_impute_task, X_test_categorical_impute_task] >> transform_categorical_train_task
[X_train_categorical_impute_task, X_test_categorical_impute_task] >> transform_categorical_test_task
