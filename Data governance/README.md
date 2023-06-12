# Data governance

In this homework we will be working with the topic of data governance. 
We will mainly be working with the DVC (data version control) tool.

To install the dvc on our machine we use the following command:
`pip install dvc`

After the installation we check for the version of the dvc with the following:
`dvc --version`

My machine has installed 2.58.2 version.

To start working with dvc we must initialize it in this particular directory.

To do that we run the following command:
`dvc init --no-scm`

Because out git is tracking the the whole repository (MLengineering) and not the Data governance folder --no-scm is necessary.
This means we have to manually coordinate all dvc actions.

First command we run from dvc here is:

`dvc run cleaning -d cleaning.py data/data.csv -o data/df_clean.csv --no-exec python cleaning.py`

dvc remote add -d myremote gdrive://1t0SBFO4vd5BrNneCMRr6TfHmvtVnY_Lo