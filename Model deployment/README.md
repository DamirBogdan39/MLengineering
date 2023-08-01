# Model deployment

In this module there are several main tasks needed to be performed to deploy the model:

- Creating the package to predict with
- Deploy the model as REST API
- Deploy the model with batch scheduling

## Packaging

To package the code `setuptools` python's package was used. 

```python
setup(
    name='thyroid_model_damir',
    version='0.1.0',
    author='Damir Bogdan',
    author_email='damribogdan39@gmail.com',
    description='Pretrained thyroid model and pipeline for classification',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'thyroid_model_damir': ['pipeline.joblib', 'label_encoder.joblib', 'raw.csv']},
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
```

In this function we define all needed to create the package, such as the package name, version, dependencies and licenses. 

After creating the `setup.py` script which contains the setup for the package creation we run the following commands in the terminal:

```bash
# Create binaries and source files for package
python setup.py sdist bdist_wheel

# Check if binaries and dependencies are available
twine check dist/*

# Publish package to pypi
twine upload dist/*
```

This will publish the package and we will be able to install it using:

```bash
pip install thyroid-model-damir
```

The package contains all necessary artifacts such as `pipeline.joblib` which will be loaded to perfrom preprocessing and prediction.

We will use `load_pipeline()` and `load_label_encoder()` functions to load the pretrained artifacts and predict with them.

### Testing

Inside of the package there is a `tests.py` script which performs testing on some of the functionalities.
For example:

```python
# Test class for checking the output of the pipeline
class TestPipePredictOutput(unittest.TestCase):

    def test_pipe_predict(self):
        result_array = pipe.predict(X)  # Call your pipe.predict() function here

        # Ensure the result is a NumPy array
        self.assertIsInstance(result_array, np.ndarray, "Expected a NumPy array, but got {type(result_array)}")

        # Check data type of elements in the array
        self.assertTrue(np.issubdtype(result_array.dtype, np.int64), "Expected int64 data type for array elements")

        # Check each value in the array
        for value in result_array:
            self.assertGreaterEqual(value, 0, f"Predicted value {value} is less than 0")
            self.assertLessEqual(value, 3, f"Predicted value {value} is greater than 3")

        print("Test passed successfully! Predicted values as intended!")
```

We have used the unittest library to perform the testing and this tests checks if the output of the pipeline is correct. As we have 4 different labels in our prediction the values can be 0, 1, 2 or 3 which this test checks for.

## REST API

### Dockerfile
For rest api FastAPI was used. 
First we created a Dockerfile to enable containerization of the fastapi app.

Most important part was to install the right packages which we do with the:
`RUN pip install --no-cache-dir -r requirements.txt`

And the requirements.txt file:

```
thyroid-model-damir-bogdan==0.1.0
fastapi==0.100.0
uvicorn==0.23.1
requests==2.31.0
pydantic==1.10.9
pandas==1.5.3
```

After the installation we must `EXPOSE 8000` which will be the port we will connect to externally from the container allowing us to send requests to the container and get predictions with the model.

### Script
`main.py` is the main script of the fast api app which we run from the start of the container runtime with the command: `CMD ["python", "main.py"]`

In the `main.py` we create the fast api app:

```{python}
app = FastAPI()
```
#### Pydantic
We use the Pydantic's BaseModel class to create our custom class which checks for our columns:

```python
class InputDataItem(BaseModel):
    age: str
    sex: str
    on_thyroxine: str
    query_on_thyroxine: str
    on_antithyroid_medication: str
    sick: str
    pregnant: str
    thyroid_surgery: str
    I131_treatment: str
    query_hypothyroid: str
    query_hyperthyroid: str
    lithium: str
    goitre: str
    tumor: str
    hypopituitary: str
    psych: str
    TSH_measured: str
    TSH: str
    T3_measured: str
    T3: str
    TT4_measured: str
    TT4: str
    T4U_measured: str
    T4U: str
    FTI_measured: str
    FTI: str
    TBG_measured: str
    TBG: str
    referral_source: str
```

All of the columns are set as strings (str) because our data preprocessig allows us to have questionmarks (?)  in any of our columns which later get replaced.

#### Endpoint

```python
# Endpoint to make predictions
@app.post("/predict/")
async def predict(data_input: list[InputDataItem]):
    try:
        # Convert the JSON data to a DataFrame with all values as strings
        input_data = [item.dict() for item in data_input]
        input_df = pd.DataFrame(input_data)

        # Make predictions with the pipeline
        predictions = pipe.predict(input_df)

        predictions_encoded = encoder.inverse_transform(predictions)

        return {"predictions": predictions_encoded.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
The endpoint for prediction uses the data_input which is list of our feature names with values.
We create the data frame and use `pipe.predict()` and also `encoder.inverse_tranfsorm()` to get the predictions.

### Running the fastapi app docker container

To successfully run this container with the created endpoint ready for prediction we must first create an image. 

To create the image use the following command from the terminal when in `REST_API` directory path:

```bash
docker build -t fastapi-image .
``` 

This will successfully build the image and next we must run the container:

```bash
docker run -d --name my_fastapi_app_container --restart always -p 8000:8000 fastapi-image
```

`--restart always` will allow us to contiunously run the container.

`-p 8000:8000` connects the host port with the container port 8000 which will recieve requests and allow us to make predictions.

We can use `request.py` script to send a request to the API which will return us:

`Predictions: ['negative']`

Or we can use the `prediction.sh` which returns us:

`{"predictions":["negative"]}`

Either way fast api is responsive and gives the predictions in under 1 second. 
This is the case for 1 sample from the data.

## Batch serving

For batch serving it is intended to use dvc pipeline as as workflow manager and cron for the scheduling.

We create a dockerfile that will create the container which will perform the prediction.

```docker
FROM python:3.10.12

# Set working directory inside the container to /app
WORKDIR /app

# Copy the current directory to /app in the container
COPY . .

# Install required libraries and DVC
RUN apt-get update && apt-get install -y cron
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --user dvc==3.3.1

# Add /root/.local/bin to the PATH
ENV PATH="/root/.local/bin:${PATH}"
```

The pipeline used is a dvc.yaml:

```yaml
stages:
  pipeline:
    cmd: python3 ../src/pipe_predict.py
    deps:
    - ../src/pipe_predict.py
    - ../data/raw/raw_data.csv
    outs:
    - ../data/predicted/pipe_predicted.csv
  encoder:
    cmd: python3 ../src/label_encode.py
    deps:
    - ../data/predicted/pipe_predicted.csv
    - ../src/label_encode.py
    outs:
    - ../data/predicted/label_predictions.csv
```

We read the in the data, perform prediction load the encoder and inverse_transform to get predicted labels.

Executing the `script.sh` creates the container and runs it in interactive mode:

```bash
docker build -t batch_serving_image .

docker run -it -d --name batch_serving_container-1 \
    -v ./data:/app/data \
    -v ./cron_logs:/app/cron_logs \
    batch_serving_image /bin/bash


docker exec -it batch_serving_container-1 /bin/bash
```

And when inside the container we run the `container_script.sh` which initalizes the dvc inside of the container. 

The `cron_script.sh` perfroms the `dvc repro -R pipelines/` which executes the pipelines and gives us the predictions. Running the `cron_script.sh` gives the `label_predictions.csv` which contains the prediction for each of the rows.

Sadly, I was not able to make cron work with this setup. I have left the name `cron_script.sh` as such because that is what cron has to execute but I have found no working solution for it.

