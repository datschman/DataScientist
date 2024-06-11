import sys
import os
import joblib
import logging

from fastapi import FastAPI, Query
import pandas as pd


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
    experience_level: int = Query(1, description="Experience level"),
    employment_type: int = Query(1, description="Employment type"),
    job_title: str = Query("Engineering", description="Job title"),
    employee_residence: str = Query("US", description="Employee residence"),
    remote_ratio: int = Query(0, description="Remote ratio"),
    company_size: int = Query(None, description="Company size"),
    company_location_grouped: str = Query(None, description="Company location grouped")
):
    try:
        # Load the real model
        model_path = os.path.join(os.path.dirname(__file__), 'models_pkl', 'real_model.pkl')
        logging.debug(f"Loading model from {model_path}")
        model = joblib.load(model_path)

        # Handle optional fields
        if company_size is None:
            company_size = 2  # Default to 'Medium' size if not provided
        if company_location_grouped is None:
            company_location_grouped = employee_residence  # Default to employee residence

        # Prepare the input data for prediction
        input_data = pd.DataFrame([[
            work_year, experience_level, employment_type, job_title,
            employee_residence, remote_ratio, company_size, company_location_grouped
        ]], columns=[
            'work_year', 'experience_level', 'employment_type', 'job_title',
            'employee_residence', 'remote_ratio', 'company_size', 'company_location_grouped'
        ])
        logging.debug(f"Input data: {input_data}")

        # Ensure correct data types
        input_data = input_data.astype({
            'work_year': 'int64',
            'experience_level': 'int64',
            'employment_type': 'int64',
            'job_title': 'object',
            'employee_residence': 'object',
            'remote_ratio': 'int64',
            'company_size': 'int64',
            'company_location_grouped': 'object'
        })
        logger.debug(f"Input data (with types): {input_data.dtypes}")

        # Make prediction
        prediction = model.predict(input_data)[0]
        logging.debug(f"Prediction: {prediction}")

        return {"prediction": prediction}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
