import pandas as pd
import numpy as np
import mlflow
import os
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

# Specify the URI
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow-server:5000"

# Your MLflow client code and experiment runs here

# Start the MLflow experiment
mlflow.set_experiment("best_model")

# Read the data
train_df = pd.read_csv('../../data/processed/train_df.csv')
test_df = pd.read_csv('../../data/processed/test_df.csv')

# Get features and target
X_train = train_df.drop('target', axis=1)
y_train = train_df['target']
X_test = test_df.drop('target', axis=1)
y_test = test_df['target']

# Encode the target variable with integer labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Get the original target names
target_names = label_encoder.classes_

# Define the hyperparameters
hyperparameters = {
    'n_estimators': 100,
    'max_depth': 5,
    'random_state': 42
}

# Create classifier
clf = XGBClassifier(**hyperparameters)

# Fit the model to the data
clf.fit(X_train, y_train_encoded)

# Predict on the test data
y_pred_encoded = clf.predict(X_test)

# Decode the predicted labels
y_pred = label_encoder.inverse_transform(y_pred_encoded)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
recall_macro = recall_score(y_test, y_pred, average='macro')
f1_macro = f1_score(y_test, y_pred, average='macro')

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=target_names)

# Plot the confusion matrix heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_names, yticklabels=target_names)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")  # Save the plot as an artifact

# Start MLflow run
with mlflow.start_run():
    # Log the model and metrics to MLflow
    mlflow.xgboost.log_model(clf, "model")
    mlflow.log_params(hyperparameters)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("recall_macro", recall_macro)
    mlflow.log_metric("f1_macro", f1_macro)
    
    # Log the confusion matrix as an artifact with the original target names
    mlflow.log_artifact("confusion_matrix.png")
