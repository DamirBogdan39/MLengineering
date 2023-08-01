
# Dependencies
import pandas as pd 
from pathlib import Path
from thyroid_model_damir_bogdan.load_label_encoder import load_label_encoder

# Get the current working directory
current_directory = Path.cwd()
    
# Get the parent directory
parent_directory = current_directory.parent

# Read the predictions
predictions = pd.read_csv(parent_directory.joinpath("data", "predicted", "pipe_predicted.csv"), names=["Class"])

# Load label encoder
le = load_label_encoder()

enc_pred = le.inverse_transform(predictions)

# Convert the NumPy array to a pandas DataFrame with one column
df = pd.DataFrame({'Class': enc_pred})

# Save the DataFrame to a CSV file
df.to_csv(parent_directory.joinpath("data", "predicted", "label_predictions.csv"), index=False)
