"""
This module contains the function needed to load the label encoder for inverse transforming the predicted values.
"""

# Dependencies
import joblib
from pathlib import Path

# Load label encoder function
def load_label_encoder():
    current_directory = Path(__file__).parent
    label_encoder_path = current_directory / "label_encoder.joblib"

    try:
        loaded_encoder = joblib.load(label_encoder_path)
        return loaded_encoder
    except FileNotFoundError:
        return "Error: The 'label_encoder.joblib' file does not exist."

