import mlflow
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
import os
import warnings

# Specify the URI
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow-server:5000"

# Your MLflow client code and experiment runs here

# Start the MLflow experiment
mlflow.set_experiment("hyperparameters")

# Read the data
train_df = pd.read_csv('../../data/processed/hyperparams_train_df.csv')
test_df = pd.read_csv('../../data/processed/hyperparams_test_df.csv')

# Get features and target
X_train = train_df.drop('target', axis=1)
y_train = train_df['target']
X_test = test_df.drop('target', axis=1)
y_test = test_df['target']

# Define the parameter grid
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10]
}

# Create classifier
clf = RandomForestClassifier(random_state=42)

# Perform grid search cross-validation
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    grid_search = GridSearchCV(clf, param_grid, cv=5)
    grid_search.fit(X_train, y_train)

# Get the best models and their hyperparameters
best_models = grid_search.cv_results_['params']
best_scores = grid_search.cv_results_['mean_test_score']

# Start MLflow run
with mlflow.start_run():
    for model_params, score in zip(best_models, best_scores):
        # Create a new classifier with the specific hyperparameters
        clf = RandomForestClassifier(random_state=42, **model_params)

        # Fit the model to the data
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        recall_macro = recall_score(y_test, y_pred, average='macro')
        f1_macro = f1_score(y_test, y_pred, average='macro')

        # Log the model and metrics to MLflow
        with mlflow.start_run(nested=True):
            mlflow.sklearn.log_model(clf, "model")
            mlflow.log_params(model_params)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("recall_macro", recall_macro)
            mlflow.log_metric("f1_macro", f1_macro)

            # Generate confusion matrix heatmap
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
            plt.xlabel("Predicted")
            plt.ylabel("True")
            plt.title("Confusion Matrix")

            # Save the heatmap as an artifact
            plt.savefig("confusion_matrix.png")
            mlflow.log_artifact("confusion_matrix.png")
