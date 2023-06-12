"""
Testing
"""

# Necessary imports
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load df_test from the saved CSV file
df_test = pd.read_csv('data/df_test.csv')

# Split df_test into X_test and y_test
X_test = df_test.drop('diagnosis', axis=1)
y_test = df_test['diagnosis']

# Load the saved model as 'clf'
clf = joblib.load('model')

# Calculate the accuracy score of the decision tree classifier on the test data
y_pred = clf.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Write to file
with open('metrics.json', 'w') as outfile:
    json.dump({"accuracy":accuracy,
               "precision":precision,
               "recall":recall,
               "f1":f1}, outfile)


# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Create a seaborn heatmap of the confusion matrix
sns.heatmap(cm, annot=True, cmap='RdPu', fmt='d', cbar=False)

# Set labels, title, and axis ticks
tick_labels = ['Benign', 'Malignant']
plt.xlabel('Predicted', fontsize=12)
plt.ylabel('True', fontsize=12)
plt.title('Confusion Matrix', fontsize=14)
plt.xticks(ticks=[0.5, 1.5], labels=tick_labels, fontsize=10, ha='center')
plt.yticks(ticks=[0.5, 1.5], labels=tick_labels, fontsize=10, va='center')

# Save the plot
plt.savefig('confusion_matrix.png', dpi=80)
