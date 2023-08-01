"""
A script that contains all necessary commands to publish the python package needed for model deployment.
"""

from setuptools import setup, find_packages

description = """
Thyroid classification package 

This package contains a sklearn pipeline that incorporates necessary preprocessing steps and a XGBoost classification model 
used to perform a classification for the Thyroid data set. 

To use the package use the following commands:

```python
# To import use:
from thyroid_model_damir_bogdan.load_pipeline import *
from thyroid_model_damir_bogdan.load_label_encoder import load_label_encoder

# To load pipeline and encoder use:
pipeline = load_pipeline()
encoder = load_label_encoder()

# To predict use:
y_pred = pipeline.predict(X) # X is a dataframe object of features
y_encoded = encoder.inverse_transform(y_pred)
```
"""
setup(
    name='thyroid_model_damir_bogdan',
    version='0.1.0',
    author='Damir Bogdan',
    author_email='damribogdan39@gmail.com',
    description='Pretrained thyroid model and pipeline for classification',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'thyroid_model_damir_bogdan': ['pipeline.joblib', 'label_encoder.joblib', 'raw.csv']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.6',
    install_requires=[  
        'numpy==1.25.0',
        'scikit-learn==1.0.2',
        'xgboost==1.7.6',
        'pandas==1.5.3',
        'joblib==1.3.1',
        'pathlib'
    ],
)
