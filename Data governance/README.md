# Data governance

In this homework we will be working with the topic of data governance. 
We will mainly be working with the DVC (data version control) tool.
Main task in this part will be to setup a remote storage for our data set we will be using, to create a pipeline that will run all our necessary scripts and to check the metrics that are important for us.

We will be using a simple breast cancer data set for the task of binary classification to check if the cancer is malignant or benign.

## Dvc initialization
To install the dvc on our machine we use the following command:

```bash
pip install dvc
```

After the installation we check for the version of the dvc with the following:

```bash
dvc --version
```

My machine has installed 2.58.2 version.

To start working with dvc we must initialize it in this particular directory.

To do that we run the following command:

```bash
dvc init
```
This part is a little tricky because we are working in a directory called `MLEngineering` but our main and only directory of interest is `Data governance`.
Because our git is initalized in the `MLEngineering` that is where we initialize the dvc also.

### Adding remote storage

Next part is setting up the remote storage where our data will be saved and with which we will link our project. 
In this case I choose google drive as remote.

Next command will link our remote storage with the project:

```bash
dvc remote add -d data_governance_remote gdrive://1BMiJklZXeXhNcl_dpKHObb__A2SUVnRT
```
Name of the storage is `data_governance_remote` and `1BMiJklZXeXhNcl_dpKHObb__A2SUVnRT` is path to the directory on google drive where the data will be stored.  It is on my personal drive with the path mydrive/data/data_governance_remote.

Running the following code:

```bash
dvc remote list
```
we get the output:

```bash
data_governance_remote  gdrive://1BMiJklZXeXhNcl_dpKHObb__A2SUVnRT
```
And we can see that our remote is connected.

## Creating a pipeline

Next part is creating the pipeline that will run our experiment.

First command we run from dvc here is:

```bash
dvc run -n cleaning -d cleaning.py data/data.csv -o data/df_clean.csv --no-exec python cleaning.py 
```
This command creates the first step in the pipeline that cleans the data hence is called `cleaning`. This is defined with the `-n`.
The `-d` defines our dependecies that are the python script `cleaning.py` and our data set called `data.csv` which is in the data directory. 
The output is a cleaned data set called `df_clean.csv` in the data directory. And the command to run this is `python cleaning.py`.

The rest of the pipeline can be found in te `dvc.yaml` file which were typed by hand. Much caution must be taken into account when creating the pipeline to define all the necessary dependencies and the outputs that a part of the pipeline produces for the pipeline to work as it is supposed to.

After the pipeline is created we can run the following command:

```bash
dvc repro
```

That will run the pipeline and produce the necessary results. 
Results are stored in the `metrics.json` file and for this problem we chose the simple metrics: accuracy, precision, recall and f1 score.

The results of this experiment are accessible with the command:

```bash
dvc metrics show
```

And if everything is working correctly they have these values:

```bash
Path                          accuracy    f1       precision    recall
Data governance/metrics.json  0.94152     0.92308  0.89552      0.95238
```

## Sending the data to remote

After everything is setup and running it is time to send the data to remote storage.

The following line inside of the Data governance directory adds the data set to be dvc tracked:

```bash
dvc add data/data.csv
```

This creates the `.gitignore` and `data.csv.dvc` files.
`.gitignore` insures us the data set will not be pushed to github when pushing the update.
The file that will be pushed is `data.csv.dvc` that will keep track of our data and allow us to pull it from remote.

As we also do not want to push the cleaned, train and test data set we will add them to the `.gitignore` file and they are tracked with the dvc because they are a part of the pipeline.

We also create a `.gitignore` file within the Data governance directory and add `model` to be ignored by the git. This demonstrates that not only data files can be tracked with dvc but binary files also. In case we had a really large model this would prove it self as very useful.

To add the data to the remote storate we execute the following command:

```bash
dvc push
```

This will upload the data to the external storage, in our case, google drive.

## Pulling the data and reproducing the experiment

After all of the the project is configued and can be pushed to git.

We add everyhting to git with:

```bash
git add .
```
commit:

```bash
git commit -m "Finished Data governance"
```

and push:

```bash
git push origin master
```

When in the github repository we can see there are no data sets and neither the model is there.
To obtain the data sets and the model we can clone the whole repository onto our machine:

```bash 
git clone git@github.com:DamirBogdan39/MLengineering.git
```

On our machine go into the `Data governance` directory, open up the terminal and run:

```bash 
dvc pull
dvc repro
dvc metrics show
```

Which will:
1. Pull the data and the model from the remote storage
2. Reproduce the pipeline 
3. Show us the same results as before

## Conclusion

This concludes the Data governance project which had the goal of demonstrating how dvc tool works and what is its purpose. 
We managed to create the pipeline, send the data to remote storage, reproduce the pipeline and show the metrics. Even though both the model and data set are rather small this methodology and approach is very useful when working with large data sets and large models.