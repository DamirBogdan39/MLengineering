
# Dependencies
from thyroid_model_damir_bogdan.load_pipeline import *
import pandas as pd 
from pathlib import Path

# Get the current working directory
current_directory = Path.cwd()
    
# Get the parent directory
parent_directory = current_directory.parent

# Get directory of the data
raw_data_path = parent_directory.joinpath("data", "raw", "raw_data.csv")

# Read the data
X = pd.read_csv(raw_data_path)

# Load the pipeline
pipe = load_pipeline()

# Predict with the pipeline
predictions = pipe.predict(X)

# Save the predictions
np.savetxt(parent_directory.joinpath("data", "predicted", "pipe_predicted.csv"), predictions, delimiter=",", fmt='%d')
