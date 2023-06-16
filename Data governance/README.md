# Data governance

In this homework we will be working with the topic of data governance. 
We will mainly be working with the DVC (data version control) tool.

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

### Adding tracking of data

```bash
dvc remote add -d data_governance_remote gdrive://1BMiJklZXeXhNcl_dpKHObb__A2SUVnRT
```

First command we run from dvc here is:

```bash
dvc run cleaning -d cleaning.py data/data.csv -o data/df_clean.csv --no-exec python cleaning.py
```