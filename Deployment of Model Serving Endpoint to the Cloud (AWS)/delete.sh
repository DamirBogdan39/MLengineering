# Delete the endpoint
aws sagemaker delete-endpoint --endpoint-name Deployment-endpoint

# Delete the endpoint configuration
aws sagemaker delete-endpoint-config --endpoint-config-name Deployment-config

# Delete the model
aws sagemaker delete-model --model-name xgb-thyroid-clf