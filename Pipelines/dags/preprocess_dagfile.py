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

from src.data.import_data import import_data
from src.data.replace_questionmarks import replace_questionmarks
from src.data.drop_constant_columns import drop_constant_columns
from src.data.recode_numeric import recode_numeric
from src.data.recode_ordinal import recode_ordinal
from src.data.clean_age_feature import clean_age_feature
from src.data.merge_features import merge_features


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


t1 = PythonOperator(
        task_id='import_data',
        python_callable=import_data,
       # op_args=[data_path],
        dag=dag,
)


t2 = PythonOperator(
    task_id='replace_questionmarks',
    python_callable=replace_questionmarks,
    dag=dag,
)

t3 = PythonOperator(
    task_id='remove_columns',
    python_callable=drop_constant_columns,
    dag=dag,
)


t4 = PythonOperator(
    task_id='recode_numeric_features',
    python_callable=recode_numeric,
    dag=dag,
)

t5 = PythonOperator(
    task_id='recode_ordinal_features',
    python_callable=recode_ordinal,
    dag=dag,
)


t6 = PythonOperator(
    task_id='clean_age_feature',
    python_callable=clean_age_feature,
    dag=dag,
)

t7 = PythonOperator(
    task_id='merge_features',
    python_callable=merge_features,
    dag=dag,
)


# Set the task dependencies
t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
t5.set_upstream(t3)
t6.set_upstream(t4)
t7.set_upstream([t5, t6])