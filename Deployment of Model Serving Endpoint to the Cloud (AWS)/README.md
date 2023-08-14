# Deployment of Model Serving Endpoint to the Cloud (AWS)

This is the last part of the Machine Learning Engineering course.

In this part we will be deploying the model inference endpoint to the AWS SageMaker.

As in previous few tasks we are working with the Thyroid classification problem.

We are working with a package I have created in a previous task called `thyroid_model_damir_bogdan` which contains all necessary code and with `FastAPI` which will serve as the API for the AWS.

## Docker image

Most important part of deploying the docker image to the ECR (elastic container repository) and making it compatble is to correctly set the `ENTRYPOINT`. Entrypoint here is set like:

```docker
ENTRYPOINT ["python", "main.py"]
```

So when the SageMaker runs the image it will run the main.py python script.
Inside the script we start the `FastAPI` api which will perform our model inference and start the `uvicorn` which will run our application - `app`.

```py
uvicorn.run(app, host="0.0.0.0", port=8080)
```

The following command explain how to push the image to AWS.

```shell
# Build the Docker image
docker build -t fastapi-deployment-image:1.0.0 .

# Tag the image
docker tag fastapi-deployment-image:1.0.0 fastapi-deployment-image:v1

# Tag the image
docker tag fastapi-deployment-image:1.0.0 ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1

# Push the Docker image to ECR
docker push ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1
```

With this commands our docker image is avaliable in the AWS and ready to be used.


## AWS CLI

All the work was done via a shell script which can be found in the reporistory (`script copy.sh`). 
All personal account info has been replaced so replication will not be possible, to replicate, you must provide own info.

To install the AWS cli to the machine run the following command.

```bash
pip install awscli --upgrade --user
```
This will allow us to use aws command from the shell to run everyhting else necessary.


To set up the account we can use:

```bash
# Configure keys to access AWS
aws configure set aws_access_key_id ACCESS_KEY
aws configure set aws_secret_access_key SECRET_KEY
aws configure set default.region eu-central-1
```

This logs us into the personal account and we are ready to create the model, endpoint configuration and endpoint.

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
```

### Model

First we create a repository with this command:

```bash
aws ecr create-repository --repository-name fastapi-deployment-image
```

And get the return:

```bash
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:eu-central-1:751398424529:repository/fastapi-deployment-image",
        "registryId": "751398424529",
        "repositoryName": "fastapi-deployment-image",
        "repositoryUri": "751398424529.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image",
        "createdAt": 1691572440.0,
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

To create the model use:

```bash
aws sagemaker create-model --model-name xgb-thyroid-clf --execution-role-arn arn:aws:iam::USER_ID:role/sagemaker-role --primary-container Image=USER_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1
```

This will set our previously pushed docker image as the primary container to run.
And the output is:

```bash
{
    "ModelArn": "arn:aws:sagemaker:eu-central-1:751398424529:model/xgb-thyroid-clf"
}
```

## Endpoint

To successfully run the endpoint we must first create the endpoint configuration. 
To do that run the following code:

```bash
aws sagemaker create-endpoint-config --endpoint-config-name Deployment-config --production-variants VariantName=deployment,ModelName=xgb-thyroid-clf,InitialInstanceCount=1,InstanceType=ml.t2.medium
```

Which returns:
```bash
 {
    "EndpointConfigArn": "arn:aws:sagemaker:eu-central-1:751398424529:endpoint-config/deployment-config"
}
```

To create the endpoint we run this command:

```bash
aws sagemaker create-endpoint --endpoint-name Deployment-endpoint --endpoint-config-name Deployment-config 
```

Which returns:

```bash
{
    "EndpointArn": "arn:aws:sagemaker:eu-central-1:751398424529:endpoint/deployment-endpoint"
}
```


## Invoking the endpoint

Finally to invoke the endpoint we run this command:

```bash
aws sagemaker-runtime invoke-endpoint --endpoint-name Deployment-endpoint --body '[{"age": "26", "sex": "F", "on_thyroxine": "f", "query_on_thyroxine": "f", "on_antithyroid_medication": "f", "sick": "f", "pregnant": "f", "thyroid_surgery": "f", "I131_treatment": "f", "query_hypothyroid": "f", "query_hyperthyroid": "f", "lithium": "f", "goitre": "f", "tumor": "f", "hypopituitary": "f", "psych": "f", "TSH_measured": "t", "TSH": "2.1", "T3_measured": "t", "T3": "2.2", "TT4_measured": "t", "TT4": "95", "T4U_measured": "t", "T4U": "1", "FTI_measured": "t", "FTI": "95", "TBG_measured": "f", "TBG": "?", "referral_source": "other"}]' --content-type "application/json" prediction.json
```
If the command runs sucessfullt we ge this as the output:

```bash
{
    "ContentType": "application/json",
    "InvokedProductionVariant": "deployment"
}
```
This is a rather long command because all the data is contained in it in a json format. 
Essentially, e send the data to the endpoint and infer on which class is and write that into the `prediction.json` file.

If we open the `prediction.json` we can see its content:

```bash
{"predictions":["negative"]}
```

With this we conclude that out model predicted this case to be `negative`.