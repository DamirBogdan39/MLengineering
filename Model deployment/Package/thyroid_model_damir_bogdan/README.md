Thyroid classification package 

This package contains a sklearn pipeline that incorporates necessary preprocessing steps and a XGBoost classification model 
used to perform a classification for the Thyroid data set. 

To use the package use the following commands:

```python
# To import use:
from thyroid_model_damir.load_pipeline import *
from thyroid_model_damir.load_label_encoder import load_label_encoder

# To load pipeline and encoder use:
pipeline = load_pipeline()
encoder = load_label_encoder()

# To predict use:
y_pred = pipeline.predict(X) # X is a dataframe object of features
y_encoded = encoder.inverse_transform(y_pred)
```