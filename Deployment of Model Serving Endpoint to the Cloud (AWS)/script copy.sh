# Install the awscli

pip install awscli --upgrade --user

# Build the Docker image
docker build -t fastapi-deployment-image:1.0.0 .

# Tag the image
docker tag fastapi-deployment-image:1.0.0 fastapi-deployment-image:v1

# Configure keys to access AWS
aws configure set aws_access_key_id ACCESS_KEY
aws configure set aws_secret_access_key SECRET_KEY
aws configure set default.region eu-central-1

# Log in to ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com

# Create a repository in ECR
aws ecr create-repository --repository-name fastapi-deployment-image

# Push the Docker image to ECR

# Tag the image
docker tag fastapi-deployment-image:1.0.0 USER_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1

# Push the Docker image to ECR
docker push USER_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1

# Create a sagemaker model
aws sagemaker create-model --model-name xgb-thyroid-clf --execution-role-arn arn:aws:iam::USER_ID:role/sagemaker-role --primary-container Image=USER_ID.dkr.ecr.eu-central-1.amazonaws.com/fastapi-deployment-image:v1

# Create an endpoint configuration
aws sagemaker create-endpoint-config --endpoint-config-name Deployment-config --production-variants VariantName=deployment,ModelName=xgb-thyroid-clf,InitialInstanceCount=1,InstanceType=ml.t2.medium

# Create an endpoint
aws sagemaker create-endpoint --endpoint-name Deployment-endpoint --endpoint-config-name Deployment-config 

# Invoke the endpoint

aws sagemaker-runtime invoke-endpoint --endpoint-name Deployment-endpoint --body '[{"age": "26", "sex": "F", "on_thyroxine": "f", "query_on_thyroxine": "f", "on_antithyroid_medication": "f", "sick": "f", "pregnant": "f", "thyroid_surgery": "f", "I131_treatment": "f", "query_hypothyroid": "f", "query_hyperthyroid": "f", "lithium": "f", "goitre": "f", "tumor": "f", "hypopituitary": "f", "psych": "f", "TSH_measured": "t", "TSH": "2.1", "T3_measured": "t", "T3": "2.2", "TT4_measured": "t", "TT4": "95", "T4U_measured": "t", "T4U": "1", "FTI_measured": "t", "FTI": "95", "TBG_measured": "f", "TBG": "?", "referral_source": "other"}]' --content-type "application/json" prediction.json
