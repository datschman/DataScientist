from fastapi import FastAPI
import pickle
from .models import DummyModel
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

@app.get("/")
def root():
    return {"greeting": "bonsoir"}

@app.get("/predict")
def predict(experience_level: int = 1, country: int = 1):
    with open("package_folder/models/dummy_model.pkl", "rb") as file:
        model = pickle.load(file)

    prediction = model.predict([[experience_level, country]])[0]

    return {"prediction": prediction}
