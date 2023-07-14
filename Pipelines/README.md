# Pipelines


## Running airflow in docker

The goal of this task was to transfer the preprocessing part from the previous task into a pipeline using Apache Airflow.

As we were working with thyroid data set I have kept the same data but one of the goals was to present the merging of data so the data set was split in two halfs and imported as such. 

Main task was to present the usage of airflow and I have opted with the approach of using the airflow from a docker container. 

The official docker compose yaml file from airflow allows us to easily set up working container for:

- postgres
- redis
- airflow-webservers
- airflow-scheduler
- airflow-worker
- airflow-triggerer
- airflow-init

One modification was needed to perform this task and that is installing the dependencies for my particular project so instead of the offical aiflow image we had to install additional packages that are states in the `requirements.txt` file.

The dockefile inside this repository does exactly that. 

With the command

```bash
docker build -t extended_airflow .
```

We create the image and exchange the offical airflow image with our newly created `extended_airflow` image in the `docker-compose.yml`.

This allows us to use all the packages necessary to create a fully funcional pipeline.

## DAG

The most important concept of apache aiflow pipeline is a DAG (directed acyclic graph) which defines the path of tasks.

We defined our DAG in the `dagfile.py` python script. It contains the definition of a dag object:

```python
dag = DAG(
    "thyroid_preprocessing_DAG",
    default_args=default_args,
    description="DAG for preprocessing pipeline",
    schedule_interval=None,
    is_paused_upon_creation=True,
)
```

With the ID called `thyroid_preprocessing_DAG`, its description and 2 more arguments.

We set the `schedule_interval` to `None` so we can manually trigger the DAG to run because no specific scheduling for running this dag was needed. It can be set to run at a specific interval in requieriments to specific needs.

### Tasks

All task are defined as object of a `PythonOperator` class which runs a specific Python function. 
Tasks are separated from the `dagfile.py` script and are all in their respectable modules inside of the `src` directory.

I will provide one task here and explaining the logic behind it.

```python
# Task 16 - impute numerical on X_test

X_test_numerical_impute_task = PythonOperator(
    task_id="X_test_numerical_impute",
    python_callable=X_test_numerical_impute,
    dag=dag,
)
```

This task is called `X_test_numerical_impute_task` which serves the purpose of imputing values to missing values in our numeric features of X_test data set.

With `task_id` keyword argument we define the id of a task which will be useful and commented upon later.
`python_callable` defines which funcion we will run an the function is called `X_test_numerical_impute`. 
`dag` states we want to use our previously defined dag object.

Let's take a look into the python function from this task and highlight some important parts.

```python
# Function to transform numerical test data
def X_test_numerical_impute(ti):
    imputer_path = ti.xcom_pull(task_ids="fit_numerical_imputer", key="imputer_path")
    
    with open(imputer_path, 'rb') as f:
        imputer = pickle.load(f)
    
    X_test_numerical_path = ti.xcom_pull(task_ids="split_X_test", key="test_numerical_path")
    X_test_numerical_df = pd.read_csv(X_test_numerical_path)
    
    X_test_numerical_imputed = imputer.transform(X_test_numerical_df)
    X_test_numerical_imputed_df = pd.DataFrame(X_test_numerical_imputed, columns=X_test_numerical_df.columns)
    
    X_test_numerical_imputed_path = os.path.join(current_dir, '../../data/interim/X_test_numerical_imputed.csv')
    X_test_numerical_imputed_df.to_csv(X_test_numerical_imputed_path, index=False)
    
    ti.xcom_push(key="X_test_numerical_imputed_path", value=X_test_numerical_imputed_path)
```

As airflow is just and orchestrator we can see that we don't actually pass any data set or models from one task to another but rather use the task instance (`ti`) to pull and push small amount of metadata.

We use the `os` module to save the paths of the data sets and models needed in this task and pull them up in the task where they are needed.

The `ti.xcom_pull()` does the pulling of the paths and `ti.xcom_push()` pushes the paths to and existing database.

Let's explaig the pushing of the data path and then later the pulling.

In this task we have used the `ti.xcom_push(key="X_test_numerical_imputed_path", value=X_test_numerical_imputed_path)`
to push the path of the imputed numerical data of the X_test. We define the key (name) of what we want to push and provide a value (actual path). 

This gets recoreded for every specific task.

When pulling we use, for example: `ti.xcom_pull(task_ids="fit_numerical_imputer", key="imputer_path")` in which we have to specify the `task_ids` and the `key`. When we specify the task_id the airflow knows where to look for the specific key and in this case it know that we have the path to the imputer which was created in the `fit_numerical_imputer` task. 

The whole pipeline is constructed out of different specific tasks that do a small operation on the data, save the data, and pass the path to the next task that does its specific operation. 

## Dependencies

We must define dependencies in the DAG so certain tasks get run before other tasks because of the logic of the problem.
To explain this I will provide a few examples of dependencies:

```python
split_dataframe_task >> [split_X_train_task, split_X_test_task]
[split_X_train_task, split_X_test_task] >> fit_ordinal_imputer_task
fit_ordinal_imputer_task >> [X_train_ordinal_impute_task, X_test_ordinal_impute_task]
```

We first split the data set into X_train, X_test, y_train and y_test using the `split_dataframe_task`.
This task has to be run before `[split_X_train_task, split_X_test_task]` this list of tasks so we use `>>` to define that.
The `split_X_train_task` and `split_X_test_task` split the data sets into categorical, numerical and ordinal features so naturally before we run the `fit_ordinal_imputer_task` we must have ordinal data ready, hence the second dependency.
The third dependecy example states that we must fit the imuter before trying to impute the missing values.

### Running the pipeline

The pipeline is run using the airflow ui which can be accessed on the `localhost:/8080` from any web browser if the docker compose file had been executed.

Ta ccess it we must log in. The docker compose file took care of creating the account for us and we can use it: both name and pass are `airflow`.

The pipeline goes through the whole process of solving our classification problem: from importing the data, cleaning, imputing, training the model, predicting on the test data and writing a report in which can be found in the `dags/reports/classification_report.txt` file in this repo.

We can see that it successfully ran and saved us a classification report with some relevant metrics for this classification problem.

Very useful feature of the airflow ui is the graph of the DAG where we can clearly see all the tasks and dependencies between them.

