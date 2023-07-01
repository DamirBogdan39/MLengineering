import mlflow
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings

# Specify the URI
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow-server:5000"

# Your MLflow client code and experiment runs here


# Start the MLflow experiment
mlflow.set_experiment("catboost")

# Read the data
train_df = pd.read_csv('../../data/processed/catboost_train_df.csv')
test_df = pd.read_csv('../../data/processed/catboost_test_df.csv')

# Get features and target
X_train = train_df.drop('target', axis=1)
y_train = train_df['target']
X_test = test_df.drop('target', axis=1)
y_test = test_df['target']

# Define the hyperparameters
hyperparameters = {
    'iterations': 100,
    'depth': 5,
    'random_state': 42
}

# Create classifier
clf = CatBoostClassifier(**hyperparameters)

# Fit the model to the data
clf.fit(X_train, y_train)

# Predict on the test data
y_pred = clf.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
recall_macro = recall_score(y_test, y_pred, average='macro')
f1_macro = f1_score(y_test, y_pred, average='macro')

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.tight_layout()

# Save the confusion matrix heatmap as an artifact
plt.savefig("confusion_matrix.png")

# Start MLflow run

with mlflow.start_run():
    # Log the model and metrics to MLflow
    mlflow.catboost.log_model(clf, "model")
    mlflow.log_params(hyperparameters)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("recall_macro", recall_macro)
    mlflow.log_metric("f1_macro", f1_macro)

    # Log the confusion matrix heatmap as an artifact
    mlflow.log_artifact("confusion_matrix.png")
