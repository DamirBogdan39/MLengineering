"""
Main script for the REST API using FastAPI with JSON input (all values as strings)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from thyroid_model_damir_bogdan.load_label_encoder import load_label_encoder
from thyroid_model_damir_bogdan.load_pipeline import *

# Load your pre-trained pipeline here, replace 'model.pkl' with your model file
pipe = load_pipeline()
encoder = load_label_encoder()

app = FastAPI()

class InputDataItem(BaseModel):
    age: str
    sex: str
    on_thyroxine: str
    query_on_thyroxine: str
    on_antithyroid_medication: str
    sick: str
    pregnant: str
    thyroid_surgery: str
    I131_treatment: str
    query_hypothyroid: str
    query_hyperthyroid: str
    lithium: str
    goitre: str
    tumor: str
    hypopituitary: str
    psych: str
    TSH_measured: str
    TSH: str
    T3_measured: str
    T3: str
    TT4_measured: str
    TT4: str
    T4U_measured: str
    T4U: str
    FTI_measured: str
    FTI: str
    TBG_measured: str
    TBG: str
    referral_source: str

# Endpoint to make predictions
@app.post("/predict/")
async def predict(data_input: list[InputDataItem]):
    try:
        # Convert the JSON data to a DataFrame with all values as strings
        input_data = [item.dict() for item in data_input]
        input_df = pd.DataFrame(input_data)

        # Make predictions with the pipeline
        predictions = pipe.predict(input_df)

        predictions_encoded = encoder.inverse_transform(predictions)

        return {"predictions": predictions_encoded.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
