import sys
import os
import joblib
import logging

from fastapi import FastAPI, Query
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

@app.get("/")
def root():
    return {"greeting": "bonsoir"}

#@app.get("/predict")
#def predict(experience_level: int = 1, country: int = 1):
#    with open("package_folder/models/dummy_model.pkl", "rb") as file:
#        model = pickle.load(file)

#    prediction = model.predict([[experience_level, country]])[0]

#    return {"prediction": prediction}

@app.get("/predict")
def predict(
    work_year: int = Query(2024, description="Work year"),
    experience_level: str = Query("EN", description="Experience level"),
    employment_type: str = Query("FT", description="Employment type"),
    job_title_cluster: str = Query("Data Scien", description="Job title"),
    remote_ratio: int = Query(0, description="Remote ratio"),
    company_size: str = Query("M", description="Company size"),
    company_location_grouped: str = Query("US", description="Company location grouped")
):
    try:
        # Load the real model
        model_path = os.path.join(os.path.dirname(__file__), 'models_pkl', 'real_model.pkl')
        logging.debug(f"Loading model from {model_path}")
        model = joblib.load(model_path)

        # Handle optional fields
        if company_size is None:
            company_size = "M"  # Default to 'Medium' size if not provided
        if company_location_grouped is None:
            company_location_grouped = "US"  # Default to employee residence

        # Prepare the input data for prediction
        input_data = pd.DataFrame([[
            work_year, experience_level, job_title_cluster,
            remote_ratio, company_size, company_location_grouped
        ]], columns=[
            'work_year', 'experience_level', 'job_title_cluster',
            'remote_ratio', 'company_size', 'company_location_grouped'
        ])
        logging.debug(f"Input data: {input_data}")

        # Ensure correct data types
        input_data = input_data.astype({
            'work_year': 'int64',
            'experience_level': 'object',
            'job_title_cluster': 'object',
            'remote_ratio': 'int64',
            'company_size': 'object',
            'company_location_grouped': 'object'
        })
        logger.debug(f"Input data (with types): {input_data.dtypes}")

         # Ensure there are no NaNs in the input data
        if input_data.isnull().values.any():
            raise ValueError("Input data contains NaNs")

        # Convert DataFrame to NumPy array
        #input_data = input_data.to_numpy()
        #logger.debug(f"Input data (as numpy array): {input_data}")

        # Transform the input data using the model's preprocessor to check for any issues
        preprocessed_input_data = model.named_steps['preprocessor'].transform(input_data)
        logger.debug(f"Preprocessed input data: {preprocessed_input_data}")

         # Make prediction
        prediction_log = model.predict(input_data)[0]
        prediction = np.exp(prediction_log) - 0.0000001
        logger.debug(f"Prediction (log-transformed): {prediction_log}")
        logger.debug(f"Prediction: {prediction}")

        return {"prediction": prediction}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
